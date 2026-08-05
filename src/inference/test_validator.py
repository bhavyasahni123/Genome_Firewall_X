import pandas as pd

from .model_loader import ModelLoader
from .feature_validator import FeatureValidator

loader = ModelLoader()

validator = FeatureValidator(
    loader.get_feature_names()
)

df = pd.DataFrame(
    {
        "Fake_Feature": [1],
        "Total_AMR_Hits": [5],
    }
)

validated, missing, extra = validator.validate(df)

print()

print("Original Features :", len(df.columns))

print("Validated Features :", len(validated.columns))

print()

print("Missing Added :", len(missing))

print("Extra Removed :", len(extra))

print()

print(validated.head())