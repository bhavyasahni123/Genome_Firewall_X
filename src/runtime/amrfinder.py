from pathlib import Path
import subprocess
import pandas as pd


class RuntimeAMRFinder:
    """
    Runs AMRFinderPlus on a single uploaded genome.
    Produces both TSV and Parquet outputs.
    """

    def __init__(self, amrfinder_binary: str = "amrfinder"):

        self.amrfinder_binary = amrfinder_binary

    def run(
        self,
        genome_file: str | Path,
        output_directory: str | Path,
    ) -> Path:

        genome_file = Path(genome_file)
        output_directory = Path(output_directory)

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        genome_name = genome_file.stem

        tsv_file = (
            output_directory /
            f"{genome_name}.tsv"
        )

        parquet_file = (
            output_directory /
            f"{genome_name}.parquet"
        )

        command = [
            self.amrfinder_binary,
            "-n",
            str(genome_file),
            "-o",
            str(tsv_file),
        ]

        print("=" * 80)
        print("Running AMRFinderPlus")
        print("=" * 80)
        print("Genome :", genome_file)
        print("Output :", tsv_file)

        subprocess.run(
            command,
            check=True,
        )

        print("Reading TSV...")

        df = pd.read_csv(
            tsv_file,
            sep="\t",
        )

        df["Genome_ID"] = genome_name

        print("Saving parquet...")

        df.to_parquet(
            parquet_file,
            index=False,
            engine="pyarrow",
        )

        print("Finished.")
        print(parquet_file)

        return parquet_file


if __name__ == "__main__":

    runner = RuntimeAMRFinder()

    output = runner.run(
        genome_file="example.fna",
        output_directory="uploads/amrfinder",
    )

    print(output)