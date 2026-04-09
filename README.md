# Crossroad Traffic Simulation

A demo project showing how to use **Python** and **[salabim](https://www.salabim.org/)** for discrete event simulation, with **web-based animation** rendered in the browser using HTML5 Canvas.

## What it does

Simulates a 4-way intersection with:

- **Traffic lights** cycling through green, yellow, red for N-S and E-W directions
- **Cars** arriving randomly from all four directions (Poisson process)
- **Queuing** at red lights and releasing on green

The simulation runs headlessly on the server. State snapshots are recorded every 0.25s of sim-time, then streamed to the browser over a WebSocket for real-time animation.

## Architecture

```
simulation.py  -->  server.py  -->  Browser Canvas
(salabim)   frames  (FastAPI +   WS  (index.html)
headless DES        WebSocket)       2D animation
```

## Quick start

```bash
# Install dependencies (uses uv)
uv sync

# Run the server
uv run python main.py

# Open http://localhost:8000 in your browser
# Click "Start Simulation" to begin
```

## Project structure

| File | Description |
|---|---|
| `simulation.py` | Salabim crossroad model: traffic lights, cars, queues, frame recording |
| `server.py` | FastAPI app with WebSocket endpoint to stream frames |
| `static/index.html` | Browser frontend: Canvas rendering of the crossroad |
| `main.py` | Entry point that launches the web server |

## Requirements

- Python >= 3.14
- Dependencies: `salabim`, `fastapi`, `uvicorn[standard]`, `websockets`