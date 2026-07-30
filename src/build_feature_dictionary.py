from pathlib import Path

import pandas as pd

INPUT_DIR = Path("outputs/amrfinder")

all_genes = set()
all_classes = set()
all_subclasses = set()
all_types = set()
all_subtypes = set()
all_methods = set()

for parquet_file in sorted(INPUT_DIR.glob("genome_*.parquet")):

    df = pd.read_parquet(parquet_file)

    all_genes.update(df["Element symbol"].dropna().unique())
    all_classes.update(df["Class"].dropna().unique())
    all_subclasses.update(df["Subclass"].dropna().unique())
    all_types.update(df["Type"].dropna().unique())
    all_subtypes.update(df["Subtype"].dropna().unique())
    all_methods.update(df["Method"].dropna().unique())

import json

OUTPUT = Path("outputs/features")
OUTPUT.mkdir(parents=True, exist_ok=True)

dictionary = {
    "genes": sorted(all_genes),
    "classes": sorted(all_classes),
    "subclasses": sorted(all_subclasses),
    "types": sorted(all_types),
    "subtypes": sorted(all_subtypes),
    "methods": sorted(all_methods),
}

with open(OUTPUT / "feature_dictionary.json", "w") as f:
    json.dump(dictionary, f, indent=4)

print("Feature dictionary saved.")