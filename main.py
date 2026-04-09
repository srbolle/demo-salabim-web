"""
Entry point: starts the FastAPI web server.
Open http://localhost:8000 in your browser and click "Start Simulation".
"""

import uvicorn
from server import app


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
