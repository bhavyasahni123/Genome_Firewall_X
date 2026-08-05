from pathlib import Path

import pandas as pd

FEATURE_FILE = Path("outputs/features/all_features.parquet")
PHENOTYPE_FILE = Path("Dataset/GenomeData.xlsx")
OUTPUT_DIR = Path("outputs/labels")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

features = pd.read_parquet(FEATURE_FILE)

phenotypes = pd.read_excel(
    PHENOTYPE_FILE,
    engine="openpyxl",
)

features["Genome_ID"] = features["Genome_ID"].astype(str)
phenotypes["Genome ID"] = phenotypes["Genome ID"].astype(str)

phenotypes = phenotypes[
    [
        "Genome ID",
        "Antibiotic",
        "Resistant Phenotype",
    ]
].dropna()

phenotypes = phenotypes[
    phenotypes["Resistant Phenotype"] != "Intermediate"
].copy()

phenotypes["Label"] = (
    phenotypes["Resistant Phenotype"]
    .map(
        {
            "Susceptible": 0,
            "Resistant": 1,
        }
    )
)

antibiotics = sorted(
    phenotypes["Antibiotic"].unique()
)

print("=" * 70)
print("Building Training Datasets")
print("=" * 70)

for antibiotic in antibiotics:

    subset = phenotypes[
        phenotypes["Antibiotic"] == antibiotic
    ]

    dataset = features.merge(
        subset[
            [
                "Genome ID",
                "Label",
            ]
        ],
        left_on="Genome_ID",
        right_on="Genome ID",
        how="inner",
    )

    dataset = dataset.drop(
        columns=["Genome ID"]
    )

    output = OUTPUT_DIR / f"{antibiotic}.parquet"

    dataset.to_parquet(
        output,
        index=False,
        engine="pyarrow",
        compression="snappy",
    )

    print()
    print(f"{antibiotic}")
    print("-" * len(antibiotic))
    print(f"Samples : {len(dataset)}")
    print(dataset["Label"].value_counts())

print()
print("=" * 70)
print("Finished")
print("=" * 70)