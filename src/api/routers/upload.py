from fastapi import APIRouter, UploadFile, File, HTTPException

from src.api.services.upload_service import UploadService

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

service = UploadService()


@router.post("/")
async def upload_genome(
    file: UploadFile = File(...)
):
    """
    Upload a genome and run the complete Genome Firewall X pipeline.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded.",
        )

    if not file.filename.lower().endswith(".fna"):
        raise HTTPException(
            status_code=400,
            detail="Only .fna files are supported.",
        )

    try:

        result = await service.process_upload(file)

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )