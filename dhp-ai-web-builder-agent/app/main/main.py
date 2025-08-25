from fastapi import FastAPI
from .routers import hello_world, page_generator, simple_generator


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Web Builder",
        description="Generate modern web applications with AI",
        version="1.0.0"
    )

    # Include routers
    app.include_router(hello_world.router)
    app.include_router(page_generator.router)
    app.include_router(simple_generator.router)

    @app.get("/healthcheck", summary="Healthcheck", tags=["healthcheck"])
    def healthcheck():
        return {"status": "OK", "service": "AI Web Builder"}

    return app


app = create_app()
