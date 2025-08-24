from fastapi import FastAPI
from .routers import hello_world


def create_app() -> FastAPI:
    app = FastAPI(title="Hello World", version="0.0.1")
    app.include_router(hello_world.router)

    @app.get("/healthcheck", summary="Healthcheck", tags=["healthcheck"])
    def healthcheck():
        return {"status": "OK"}

    return app


app = create_app()
