import json
from pathlib import Path
from llmgt.utils.paths import get_experimental_config_path


def load_experiment_config(name: str = "experiments_det.json") -> dict[str, dict]:
    """
    Loads and validates a dictionary of experiment configs from CONFIG/experimental_config/.

    Parameters:
        name (str): The filename of the prompt_config (default: experiments_det.json)

    Returns:
        dict[str, dict]: A dictionary mapping experiment names to configs.
    """
    path = get_experimental_config_path(name)

    if not path.exists():
        raise FileNotFoundError(f"Could not find experiment prompt_config at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("Expected top-level prompt_config to be a dict of named experiments.")

    for name, cfg in data.items():
        required_keys = ["json_path", "seed", "generation_config", "batch_size", "message_keys"]
        missing = [k for k in required_keys if k not in cfg]
        if missing:
            raise ValueError(f"Experiment '{name}' is missing required keys: {missing}")
        if "id" not in cfg:
            cfg["id"] = name

    return data
