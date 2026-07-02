





How does the html5 canvas compare to the built in graphical animation in salabim?

### Planner Response

Here's a comparison:

| Aspect | Salabim built-in animation | HTML5 Canvas (our approach) |
|---|---|---|
| **Rendering** | Tkinter window (desktop) | Browser (any device) |
| **Setup** | Almost zero — use `AnimateRectangle`, `AnimateCircle` etc. directly in sim code | Separate frontend file, WebSocket plumbing |
| **Code location** | Animation mixed into simulation code | Animation fully decoupled from simulation |
| **Real-time sync** | Built-in — animation syncs to sim clock automatically | Manual — we stream frames and pace them |
| **Interactivity** | Basic buttons/sliders via `AnimateButton`, speed control | Full HTML/JS — anything you want |
| **Sharing/deployment** | Requires Python + tkinter on viewer's machine | Just a URL — works anywhere |
| **Shape drawing** | `AnimateRectangle(spec=(...))`, `AnimateCircle(radius=...)` | `ctx.fillRect()`, `ctx.arc()` — very similar |
| **Dynamic updates** | Pass lambdas for position: `x=lambda: car.x` | Send x,y each frame |
| **Performance** | Good for ~100s of objects | Good for ~1000s of objects |
| **Video export** | Built-in `video()` support | Need screen recording or canvas capture |
| **3D** | Supported (via OpenGL) | Would need Three.js or similar |
| **Dependencies** | Just salabim (+ tkinter) | FastAPI, uvicorn, websockets |

### Key tradeoff

**Salabim's animation is dramatically simpler to code.** Our entire [index.html](file:///home/srbolle/src/jobb/test_sim/static/index.html:0:0-0:0) (drawing roads, cars, lights) plus [server.py](file:///home/srbolle/src/jobb/test_sim/server.py:0:0-0:0) (WebSocket streaming) would be ~15 lines with salabim:

```python
# Hypothetical salabim-native equivalent
sim.AnimateRectangle(spec=lambda: (car.x-8, car.y-11, car.x+8, car.y+11),
                     fillcolor='blue')
```

vs our approach needing Canvas draw calls + WebSocket setup + frame recording.

**But our approach wins on deployment and flexibility** — no tkinter needed, works in a browser, fully customizable UI, easy to share.

### Bottom line

- **Prototyping / personal use** → salabim's built-in animation is faster to build
- **Sharing with others / web deployment / custom UI** → Canvas is the better choice
- **Our project as a demo** → the Canvas approach makes sense because it shows how to bridge simulation and web visualization, which is the educational purpose
