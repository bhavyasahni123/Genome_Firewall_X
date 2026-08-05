from pydantic import BaseModel

class BatchPredictionRequest(BaseModel):
    feature_file: str
    
class PredictionRequest(BaseModel):
    feature_file: str

class ExplainRequest(BaseModel):

    feature_file: str

    genome_id: str

    antibiotic: str


class HealthResponse(BaseModel):
    status: str
    models: int
    version: str

from fastapi import UploadFile, File


class UploadResponse(BaseModel):
    genome_id: str
    summary: dict
    predictions: dict
    explanation: dict