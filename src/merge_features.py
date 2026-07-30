from pathlib import Path

import pandas as pd

INPUT_DIR = Path("outputs/features")
OUTPUT_FILE = INPUT_DIR / "all_features.parquet"

feature_files = sorted(
    INPUT_DIR.glob("genome_*_features.parquet")
)

frames = []

for file in feature_files:

    print(f"Loading {file.name}")

    df = pd.read_parquet(file)

    frames.append(df)

all_features = pd.concat(
    frames,
    ignore_index=True,
)

all_features.to_parquet(
    OUTPUT_FILE,
    index=False,
    engine="pyarrow",
    compression="snappy",
)

print()
print("=" * 60)
print("Merge Complete")
print("=" * 60)
print(f"Rows    : {len(all_features)}")
print(f"Columns : {len(all_features.columns)}")
print(f"Output  : {OUTPUT_FILE}")