import threading
from typing import Optional

from fastapi import FastAPI, Response
import uvicorn

try:
	from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, generate_latest
	from prometheus_client import multiprocess
	_PROM_AVAILABLE = True
except Exception:  # pragma: no cover
	_PROM_AVAILABLE = False


def start_health_app(host: str = "0.0.0.0", port: int = 8080) -> None:
	app = FastAPI()

	@app.get("/healthz")
	def health() -> dict:
		return {"status": "ok"}

	if _PROM_AVAILABLE:
		@app.get("/metrics")
		def metrics() -> Response:  # type: ignore[override]
			registry = CollectorRegistry()
			try:
				multiprocess.MultiProcessCollector(registry)
			except Exception:
				pass
			data = generate_latest(registry)
			return Response(content=data, media_type=CONTENT_TYPE_LATEST)

	server = uvicorn.Server(
		config=uvicorn.Config(app=app, host=host, port=port, log_level="info")
	)

	thread = threading.Thread(target=server.run, daemon=True)
	thread.start()

