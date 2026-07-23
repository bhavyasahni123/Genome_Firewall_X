import json
from pathlib import Path
from config import GENOME_DIR, OUTPUT_DIR, GENOME_EXTENSION

DISCOVERY_DIR = OUTPUT_DIR / "discovery"
DISCOVERY_DIR.mkdir(exist_ok=True)

GENOME_LIST = DISCOVERY_DIR / "genome_list.json"
REPORT = DISCOVERY_DIR / "discovery_report.json"


def natural_key(text):
    import re
    return [int(c) if c.isdigit() else c.lower()
            for c in re.split(r'(\d+)', text)]


def discover():

    genomes = []
    folders = {}

    for folder in sorted(
        GENOME_DIR.glob("genome_*"),
        key=lambda x: natural_key(x.name)
    ):

        count = 0

        for file in folder.rglob(f"*{GENOME_EXTENSION}"):

            genomes.append(
                {
                    "genome_id": file.stem,
                    "folder": folder.name,
                    "path": str(file.resolve())
                }
            )

            count += 1

        folders[folder.name] = count

    with open(GENOME_LIST, "w") as f:
        json.dump(genomes, f, indent=2)

    report = {
        "total_folders": len(folders),
        "total_genomes": len(genomes),
        "folders": folders
    }

    with open(REPORT, "w") as f:
        json.dump(report, f, indent=2)

    print("=" * 60)
    print("Genome Firewall X")
    print("=" * 60)
    print(f"Folders Found : {len(folders)}")
    print(f"Genomes Found : {len(genomes)}")
    print("=" * 60)

    for k, v in folders.items():
        print(f"{k:<12} : {v}")

    print("\nSaved:")
    print(GENOME_LIST)
    print(REPORT)


if __name__ == "__main__":
    discover()