from fastapi import APIRouter, HTTPException

from src.api.schemas import BatchPredictionRequest
from src.api.services.batch_prediction_service import BatchPredictionService

router = APIRouter()

service = BatchPredictionService()


@router.post("/batch_predict")
def batch_predict(request: BatchPredictionRequest):

    try:

        return service.predict(request.feature_file)

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )