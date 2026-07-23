from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

GENOME_DIR = Path(
    os.environ.get(
        "GENOME_DIR",
        "/mnt/c/Users/bhavy/Downloads/Genome_Firewall_X/Ecoil_Genome_datasetBVbrc"
    )
)

RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

OUTPUT_DIR = PROJECT_ROOT / "outputs"
MODEL_DIR = PROJECT_ROOT / "models"
LOG_DIR = PROJECT_ROOT / "logs"
TEMP_DIR = OUTPUT_DIR / "temp"

for folder in [
    OUTPUT_DIR,
    MODEL_DIR,
    LOG_DIR,
    TEMP_DIR,
    RAW_DIR,
    PROCESSED_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)

AMRFINDER = "amrfinder"

MAX_WORKERS = max(8, os.cpu_count())

FLUSH_INTERVAL = 200

GENOME_EXTENSION = ".fna"