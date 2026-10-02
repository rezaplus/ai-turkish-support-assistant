from fastapi import FastAPI

from app.api.router import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Turkish Support Assistant API",
        version="1.0.0",
    )

    app.include_router(api_router)

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()
