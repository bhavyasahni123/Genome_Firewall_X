from fastapi import APIRouter, HTTPException

from src.api.schemas import PredictionRequest
from src.api.services.prediction_service import PredictionService

router = APIRouter()

service = PredictionService()


@router.post("/predict")
def predict(request: PredictionRequest):

    try:

        return service.predict_file(
            request.feature_file
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )