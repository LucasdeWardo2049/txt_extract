from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    RAW_TXT_DIR = BASE_DIR / "data/raw_txt"
    VALIDATION_DIR = BASE_DIR / "data/validation"
    DOCUMENTS_DIR = BASE_DIR / "data/documents"
    PROCESSED_DIR = BASE_DIR / "data/processed"
