import json
from pathlib import Path
from datasets import Dataset
from transformers import GenerationConfig


def load_dataset(path: Path) -> Dataset:
    """
    Load a JSON dataset into HuggingFace Dataset.
    """
    return Dataset.from_json(str(path))


def load_generation_config(cfg: dict) -> GenerationConfig:
    """
    Build a HuggingFace GenerationConfig from config dict.
    """
    return GenerationConfig(**cfg["generation_config"])


def save_dataset_json(ds, path: Path):
    """
    Save a JSON dataset into HuggingFace Dataset.
    """
    ds.to_json(str(path), orient="records", lines=True)