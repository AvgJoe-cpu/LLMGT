from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]

def get_pipeline_data_dir() -> Path:
    return get_project_root() / "pipeline_data"

def get_data_path(subdir: str, name: str = "") -> Path:
    path = get_pipeline_data_dir() / subdir
    return path / name if name else path

def get_stage_path(stage: str, name: str = "") -> Path:
    base = get_pipeline_data_dir() / "stages" / stage
    return base / name if name else base



#####
def get_output_key(msg_key):
    return f"output_{msg_key}"

def enrich_paths(config: dict, base_cache=Path("./cache"), base_results=Path("./predictions")) -> dict:
    exp_id = config.get("id", "unnamed")
    paths = {}

    for msg_key in config["message_keys"]:
        key = get_output_key(msg_key)
        paths[msg_key] = {
            "cache": base_cache / f"{exp_id}_ds_{key}",
            "arrow": base_cache / f"{exp_id}_{key}.arrow",
            "json": base_results / f"{exp_id}_{key}.json"
        }

    config["paths"] = paths
    return config

# utils/paths.py
