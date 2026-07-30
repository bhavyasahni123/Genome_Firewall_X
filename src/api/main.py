from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.health import router as health_router
from src.api.routers.predict import router as predict_router
from src.api.routers.metrics import router as metrics_router
from src.api.routers.models import router as models_router
from src.api.routers.batch_predict import router as batch_predict_router
from src.api.routers.explain import router as explain_router
from src.api.routers.upload import router as upload_router

app = FastAPI(
    title="Genome Firewall X API",
    version="1.0.0",
    description="AI-powered Antimicrobial Resistance Prediction Platform",
)

# ----------------------------------------------------
# CORS
# ----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://192.168.1.43:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health_router)
app.include_router(predict_router)
app.include_router(metrics_router)
app.include_router(models_router)
app.include_router(batch_predict_router)
app.include_router(explain_router)
app.include_router(upload_router)


@app.get("/")
def root():
    return {
        "message": "Genome Firewall X API",
        "status": "running",
    }