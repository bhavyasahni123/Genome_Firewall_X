from fastapi import APIRouter, HTTPException

from src.api.schemas import ExplainRequest
from src.api.services.explain_service import ExplainService

router = APIRouter()

service = ExplainService()


@router.post("/explain")
def explain(request: ExplainRequest):

    try:

        return service.explain(
            request.feature_file,
            request.genome_id,
            request.antibiotic,
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )