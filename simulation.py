"""
Salabim crossroad simulation with traffic lights and cars.

The simulation models a 4-way intersection with:
- Two traffic light phases (North-South green / East-West green)
- Cars arriving from all four directions
- Cars waiting at red lights and proceeding on green

State is recorded at regular intervals so it can be streamed to a web frontend.
"""

import salabim as sim
from dataclasses import dataclass, field, asdict


# ---------------------------------------------------------------------------
# Data structures for recording animation frames
# ---------------------------------------------------------------------------

@dataclass
class CarState:
    id: str
    x: float
    y: float
    direction: str  # "north", "south", "east", "west"
    waiting: bool


@dataclass
class TrafficLightState:
    direction: str  # "ns" or "ew"
    color: str  # "green", "yellow", "red"


@dataclass
class Frame:
    time: float
    cars: list[CarState] = field(default_factory=list)
    lights: list[TrafficLightState] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Simulation parameters
# ---------------------------------------------------------------------------

# Road layout constants (abstract coordinates, mapped to pixels in frontend)
ROAD_CENTER_X = 400
ROAD_CENTER_Y = 300
ROAD_HALF_WIDTH = 30  # half-width of each lane
STOP_LINE_OFFSET = 80  # distance from center to stop line
CAR_LENGTH = 20
CAR_SPACING = 28

# Timing
GREEN_TIME = 30
YELLOW_TIME = 5
CAR_SPEED = 3  # units per time step when moving
ARRIVAL_RATE_MEAN = 4  # mean inter-arrival time per direction

# Simulation
SIM_DURATION = 600  # simulation seconds
FRAME_INTERVAL = 0.25  # record a frame every N sim-seconds


# ---------------------------------------------------------------------------
# Global frame recorder
# ---------------------------------------------------------------------------

frames: list[dict] = []


def record_frame(env, traffic_light_controller, car_components):
    """Snapshot the current simulation state into a frame dict."""
    light_states = traffic_light_controller.get_light_states()
    car_states = []
    for car in list(car_components):
        car_states.append(CarState(
            id=car.name(),
            x=car.x,
            y=car.y,
            direction=car.direction,
            waiting=car.waiting,
        ))
    f = Frame(time=round(env.now(), 2), cars=car_states, lights=light_states)
    frames.append(asdict(f))


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------

class TrafficLightController(sim.Component):
    """Controls the two traffic-light phases: NS and EW."""

    def setup(self):
        self.ns_state = "green"
        self.ew_state = "red"

    def get_light_states(self) -> list[TrafficLightState]:
        return [
            TrafficLightState(direction="ns", color=self.ns_state),
            TrafficLightState(direction="ew", color=self.ew_state),
        ]

    def is_green(self, direction: str) -> bool:
        if direction in ("north", "south"):
            return self.ns_state == "green"
        else:
            return self.ew_state == "green"

    def process(self):
        while True:
            # NS green phase
            self.ns_state = "green"
            self.ew_state = "red"
            self.hold(GREEN_TIME)

            # NS yellow
            self.ns_state = "yellow"
            self.hold(YELLOW_TIME)

            # EW green phase
            self.ns_state = "red"
            self.ew_state = "green"
            self.hold(GREEN_TIME)

            # EW yellow
            self.ew_state = "yellow"
            self.hold(YELLOW_TIME)


class Car(sim.Component):
    """A car approaching the intersection from a given direction."""

    def setup(self, direction: str, controller: TrafficLightController,
              car_set: set, queues: dict):
        self.direction = direction
        self.controller = controller
        self.car_set = car_set
        self.queues = queues
        self.waiting = False
        self.car_set.add(self)

        # Starting position (off-screen, approaching)
        # Cars approach the center and stop at the stop line
        spawn_offset = 350
        if direction == "north":
            self.x = ROAD_CENTER_X + ROAD_HALF_WIDTH // 2
            self.y = ROAD_CENTER_Y + spawn_offset
        elif direction == "south":
            self.x = ROAD_CENTER_X - ROAD_HALF_WIDTH // 2
            self.y = ROAD_CENTER_Y - spawn_offset
        elif direction == "east":
            self.x = ROAD_CENTER_X + spawn_offset
            self.y = ROAD_CENTER_Y - ROAD_HALF_WIDTH // 2
        elif direction == "west":
            self.x = ROAD_CENTER_X - spawn_offset
            self.y = ROAD_CENTER_Y + ROAD_HALF_WIDTH // 2

    def _stop_line_reached(self) -> bool:
        """Check if car has reached the stop line."""
        if self.direction == "north":
            return self.y <= ROAD_CENTER_Y + STOP_LINE_OFFSET
        elif self.direction == "south":
            return self.y >= ROAD_CENTER_Y - STOP_LINE_OFFSET
        elif self.direction == "east":
            return self.x <= ROAD_CENTER_X + STOP_LINE_OFFSET
        elif self.direction == "west":
            return self.x >= ROAD_CENTER_X - STOP_LINE_OFFSET
        return False

    def _is_off_screen(self) -> bool:
        return (self.x < -50 or self.x > 850 or
                self.y < -50 or self.y > 650)

    def _queue_position(self) -> int:
        """Return position in queue (0 = front)."""
        q = self.queues[self.direction]
        members = list(q)
        if self in members:
            return members.index(self)
        return -1

    def _stop_y_for_queue_pos(self, pos: int) -> float:
        if self.direction == "north":
            return ROAD_CENTER_Y + STOP_LINE_OFFSET + pos * CAR_SPACING
        elif self.direction == "south":
            return ROAD_CENTER_Y - STOP_LINE_OFFSET - pos * CAR_SPACING
        return self.y

    def _stop_x_for_queue_pos(self, pos: int) -> float:
        if self.direction == "east":
            return ROAD_CENTER_X + STOP_LINE_OFFSET + pos * CAR_SPACING
        elif self.direction == "west":
            return ROAD_CENTER_X - STOP_LINE_OFFSET - pos * CAR_SPACING
        return self.x

    def process(self):
        q = self.queues[self.direction]

        # Phase 1: Drive toward stop line
        while not self._stop_line_reached():
            if self.direction == "north":
                self.y -= CAR_SPEED
            elif self.direction == "south":
                self.y += CAR_SPEED
            elif self.direction == "east":
                self.x -= CAR_SPEED
            elif self.direction == "west":
                self.x += CAR_SPEED
            self.hold(FRAME_INTERVAL)

        # Phase 2: Enter queue and wait for green
        self.enter(q)
        self.waiting = True

        while True:
            pos = self._queue_position()
            # Snap to queue position
            if self.direction in ("north", "south"):
                self.y = self._stop_y_for_queue_pos(pos)
            else:
                self.x = self._stop_x_for_queue_pos(pos)

            if pos == 0 and self.controller.is_green(self.direction):
                break
            self.hold(FRAME_INTERVAL)

        self.leave(q)
        self.waiting = False

        # Phase 3: Drive through and out
        while not self._is_off_screen():
            if self.direction == "north":
                self.y -= CAR_SPEED
            elif self.direction == "south":
                self.y += CAR_SPEED
            elif self.direction == "east":
                self.x -= CAR_SPEED
            elif self.direction == "west":
                self.x += CAR_SPEED
            self.hold(FRAME_INTERVAL)

        # Cleanup
        self.car_set.discard(self)


class CarGenerator(sim.Component):
    """Generates cars arriving from a specific direction."""

    def setup(self, direction: str, controller: TrafficLightController,
              car_set: set, queues: dict):
        self.direction = direction
        self.controller = controller
        self.car_set = car_set
        self.queues = queues

    def process(self):
        while True:
            Car(direction=self.direction,
                controller=self.controller,
                car_set=self.car_set,
                queues=self.queues)
            self.hold(sim.Exponential(ARRIVAL_RATE_MEAN).sample())


class FrameRecorder(sim.Component):
    """Records simulation state at regular intervals."""

    def setup(self, controller: TrafficLightController, car_set: set):
        self.controller = controller
        self.car_set = car_set

    def process(self):
        while True:
            record_frame(self.env, self.controller, self.car_set)
            self.hold(FRAME_INTERVAL)


# ---------------------------------------------------------------------------
# Run simulation
# ---------------------------------------------------------------------------

def run_simulation() -> list[dict]:
    """Run the crossroad simulation and return recorded frames."""
    global frames
    frames = []

    env = sim.Environment(trace=False)

    controller = TrafficLightController()
    car_set: set = set()
    queues = {
        "north": sim.Queue("queue_north"),
        "south": sim.Queue("queue_south"),
        "east": sim.Queue("queue_east"),
        "west": sim.Queue("queue_west"),
    }

    for direction in ("north", "south", "east", "west"):
        CarGenerator(direction=direction,
                     controller=controller,
                     car_set=car_set,
                     queues=queues)

    FrameRecorder(controller=controller, car_set=car_set)

    env.run(till=SIM_DURATION)

    print(f"Simulation complete: {len(frames)} frames recorded over {SIM_DURATION}s")
    return frames


if __name__ == "__main__":
    result = run_simulation()
    print(f"First frame: {result[0]}")
    print(f"Last frame: {result[-1]}")
