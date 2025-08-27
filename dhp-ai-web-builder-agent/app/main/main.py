from fastapi import FastAPI
from .routers import page_generator, simple_generator, process
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Web Builder",
        description="Generate modern web applications with AI",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(page_generator.router)
    app.include_router(simple_generator.router)
    app.include_router(process.router)
    return app


app = create_app()
