from pathlib import Path
import json

import pandas as pd


class FeatureEngine:

    def __init__(self):
        self.feature_dir = Path("features")

        self.input_dir = Path("outputs/amrfinder")

        self.output_dir = Path("outputs/features")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.feature_dir / "feature_dictionary.json"
        ) as f:

            d = json.load(f)

        self.genes = d["genes"]

        self.feature_map = {
            "Class": d["classes"],
            "Subclass": d["subclasses"],
            "Type": d["types"],
            "Subtype": d["subtypes"],
            "Method": d["methods"],
        }

    def crosstab(
        self,
        df,
        col,
        cols,
        binary=False,
        suffix="",
    ):

        t = (
            pd.crosstab(
                df["Genome_ID"],
                df[col],
            )
            .reindex(
                columns=cols,
                fill_value=0,
            )
        )

        if binary:

            t = (t > 0).astype("uint8")

        if suffix:

            t.columns = [
                f"{c}{suffix}"
                for c in t.columns
            ]

        return t

    def build(
        self,
        parquet_file,
    ):

        parquet_file = Path(parquet_file)

        print(f"Processing {parquet_file.name}")

        df = pd.read_parquet(parquet_file)

        feat = (
            df.groupby("Genome_ID")
            .agg(
                Total_AMR_Hits=("Genome_ID", "size"),
                Unique_AMR_Genes=("Element symbol", "nunique"),
                Unique_Classes=("Class", "nunique"),
                Unique_Subclasses=("Subclass", "nunique"),
                Unique_Types=("Type", "nunique"),
                Unique_Subtypes=("Subtype", "nunique"),
                Unique_Methods=("Method", "nunique"),
                Unique_Contigs=("Contig id", "nunique"),
            )
            .reset_index()
        )

        feat = feat.merge(
            self.crosstab(
                df,
                "Element symbol",
                self.genes,
                True,
            ),
            on="Genome_ID",
        )

        feat = feat.merge(
            self.crosstab(
                df,
                "Element symbol",
                self.genes,
                False,
                "_Count",
            ),
            on="Genome_ID",
        )

        for col, vals in self.feature_map.items():

            t = self.crosstab(
                df,
                col,
                vals,
            )

            t.columns = [
                f"{col}_{c}"
                for c in t.columns
            ]

            feat = feat.merge(
                t,
                on="Genome_ID",
            )

        stats = [
            (
                ["% Identity to reference"],
                ["mean", "min", "max", "std"],
                "Identity",
            ),
            (
                ["% Coverage of reference"],
                ["mean", "min", "max", "std"],
                "Coverage",
            ),
            (
                ["Alignment length"],
                ["mean", "min", "max", "sum"],
                "Alignment",
            ),
            (
                ["Target length"],
                ["mean", "max", "sum"],
                "Target",
            ),
            (
                ["Reference sequence length"],
                ["mean", "max", "sum"],
                "Reference",
            ),
        ]

        for cols, aggs, prefix in stats:

            s = (
                df.groupby("Genome_ID")[cols[0]]
                .agg(aggs)
                .fillna(0)
            )

            s.columns = [
                f"{prefix}_{c.title()}"
                for c in s.columns
            ]

            feat = feat.merge(
                s,
                on="Genome_ID",
            )

        strand = pd.crosstab(
            df["Genome_ID"],
            df["Strand"],
        )

        strand.columns = [
            f"Strand_{c}"
            for c in strand.columns
        ]

        feat = feat.merge(
            strand,
            on="Genome_ID",
            how="left",
        )

        contig = (
            df.groupby(
                [
                    "Genome_ID",
                    "Contig id",
                ]
            )
            .size()
            .groupby("Genome_ID")
            .agg(
                Avg_Hits_Per_Contig="mean",
                Max_Hits_Per_Contig="max",
                Contigs_With_AMR="count",
            )
        )

        feat = feat.merge(
            contig,
            on="Genome_ID",
            how="left",
        )

        feat.fillna(0, inplace=True)

        out = (
            self.output_dir
            / f"{parquet_file.stem}_features.parquet"
        )

        feat.to_parquet(
            out,
            index=False,
            engine="pyarrow",
            compression="snappy",
        )

        print(f"Saved {out.name}")

        return out

    def build_all(self):

        for file in sorted(
            self.input_dir.glob(
                "genome_*.parquet"
            )
        ):

            self.build(file)


if __name__ == "__main__":

    FeatureEngine().build_all()

    print("Feature extraction completed.")