"""
FastAPI server that runs the salabim simulation and streams
animation frames to the browser via WebSocket.
"""

import asyncio
import json
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from simulation import run_simulation, FRAME_INTERVAL

app = FastAPI(title="Crossroad Simulation")

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def index():
    return HTMLResponse((STATIC_DIR / "index.html").read_text())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        # Wait for client to send "start" message
        msg = await websocket.receive_text()
        if msg != "start":
            await websocket.close()
            return

        # Run simulation in a thread so we don't block the event loop
        loop = asyncio.get_event_loop()
        frames = await loop.run_in_executor(None, run_simulation)

        # Send total frame count so client can show progress
        await websocket.send_text(json.dumps({
            "type": "init",
            "total_frames": len(frames),
            "frame_interval": FRAME_INTERVAL,
        }))

        # Stream frames with real-time pacing
        for frame in frames:
            await websocket.send_text(json.dumps({
                "type": "frame",
                "data": frame,
            }))
            await asyncio.sleep(FRAME_INTERVAL / 4)  # 4x real-time playback

        await websocket.send_text(json.dumps({"type": "done"}))

    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
