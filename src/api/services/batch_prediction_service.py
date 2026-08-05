from src.api.services.prediction_service import PredictionService


class BatchPredictionService:

    def __init__(self):

        self.service = PredictionService()

    def predict(self, feature_file):

        return self.service.predict_file(feature_file)