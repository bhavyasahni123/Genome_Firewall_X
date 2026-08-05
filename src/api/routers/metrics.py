from fastapi import APIRouter, HTTPException

from src.api.services.metrics_service import MetricsService

router = APIRouter()

service = MetricsService()


@router.get("/metrics")
def metrics():

    return service.get_metrics()


@router.get("/metrics/{antibiotic}")
def metric(antibiotic: str):

    result = service.get_metric(antibiotic)

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Antibiotic not found."
        )

    return result