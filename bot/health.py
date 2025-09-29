import threading
from typing import Optional

from fastapi import FastAPI
import uvicorn


def start_health_app(host: str = "0.0.0.0", port: int = 8080) -> None:
    app = FastAPI()

    @app.get("/healthz")
    def health() -> dict:
        return {"status": "ok"}

    server = uvicorn.Server(
        config=uvicorn.Config(app=app, host=host, port=port, log_level="info")
    )

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

