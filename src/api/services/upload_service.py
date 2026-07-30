from pathlib import Path
import shutil
import uuid

from fastapi import UploadFile

from src.runtime.pipeline import RuntimePipeline


class UploadService:

    def __init__(self):

        self.upload_dir = Path("uploads/genomes")
        self.upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.pipeline = RuntimePipeline()

    async def save_upload(
        self,
        file: UploadFile,
    ):

        genome_id = str(uuid.uuid4())

        save_path = (
            self.upload_dir /
            f"{genome_id}.fna"
        )

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        return genome_id, save_path

    async def process_upload(
        self,
        file: UploadFile,
    ):

        genome_id, genome_path = await self.save_upload(file)

        result = self.pipeline.run(
            genome_path,
        )

        result["genome_id"] = genome_id

        return result