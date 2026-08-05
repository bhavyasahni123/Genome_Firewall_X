from fastapi import APIRouter, HTTPException

from src.api.services.model_service import ModelService

router = APIRouter()

service = ModelService()


@router.get("/models")
def models():

    return service.get_models()


@router.get("/models/{antibiotic}")
def model(antibiotic: str):

    result = service.get_model(antibiotic)

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Model not found.",
        )

    return result