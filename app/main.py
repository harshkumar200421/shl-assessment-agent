from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.health import router as health_router

app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "SHL Assessment Recommendation API is running",
        "docs": "/docs",
        "health": "/health"
    }

app.include_router(chat_router)
app.include_router(health_router)