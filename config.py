from pathlib import Path

DATA_PATH = Path(__file__).parent / "data"
MODELS_PATH = Path(__file__).parent / "models"
EXPORTS_PATH = Path(__file__).parent / "exports"

# create directories if they don't exist
DATA_PATH.mkdir(exist_ok=True)
MODELS_PATH.mkdir(exist_ok=True)
EXPORTS_PATH.mkdir(exist_ok=True)