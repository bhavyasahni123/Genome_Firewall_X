import pandas as pd


class FeatureValidator:

    def __init__(self, feature_names):
        self.feature_names = feature_names

    def validate(self, features):

        if not isinstance(features, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")

        validated = features.copy()

        # -------------------------
        # Find missing features
        # -------------------------
        missing = [
            feature
            for feature in self.feature_names
            if feature not in validated.columns
        ]

        # Add all missing columns at once
        if missing:
            missing_df = pd.DataFrame(
                0,
                index=validated.index,
                columns=missing,
                dtype="float32",
            )

            validated = pd.concat(
                [validated, missing_df],
                axis=1,
            )

        # -------------------------
        # Find extra features
        # -------------------------
        extra = [
            feature
            for feature in validated.columns
            if feature not in self.feature_names
        ]

        if extra:
            validated = validated.drop(columns=extra)

        # -------------------------
        # Ensure exact training order
        # -------------------------
        validated = validated.reindex(
            columns=self.feature_names,
            fill_value=0,
        )

        # -------------------------
        # Final cleanup
        # -------------------------
        validated = validated.fillna(0)
        validated = validated.astype("float32")

        return validated, missing, extra