from pathlib import Path
import os

def get_project_root() -> Path:
    """
    Return the root path of the project repository.
    """
    return Path(__file__).resolve().parents[3]

def get_pipeline_data_dir() -> Path:
    """
    Return the path to the pipeline_data/ directory.
    """
    return get_project_root() / "pipeline_data"

def get_data_path(subdir: str, name: str = "") -> Path:
    """
    Return a path under pipeline_data/<subdir>/<name>.

    Args:
        subdir: Subdirectory inside pipeline_data/
        name: Optional file or subfolder name

    Returns:
        Resolved path to the requested file or folder
    """
    path = get_pipeline_data_dir() / subdir
    return path / name if name else path

def get_stage_path(stage: str, name: str = "") -> Path:
    """
    Return a path under pipeline_data/stages/<stage>/<name>.

    Args:
        stage: Name of the stage (e.g., "games", "prompts", "predictions")
        name: Optional filename or subdirectory

    Returns:
        Resolved path to the stage-specific target
    """
    base = get_pipeline_data_dir() / "stages" / stage
    return base / name if name else base


def ensure_parent_dir(path: Path):
    os.makedirs(path.parent, exist_ok=True)

#####
def get_output_key(msg_key):
    return f"output_{msg_key}"

def enrich_paths(config: dict) -> dict:
    """
    Attach output JSON paths (per message key) to the config.
    Uses the 'predictions' stage directory under pipeline_data/stages/.
    """
    exp_id = config.get("id", "unnamed")
    output_dir = get_stage_path("predictions")

    paths = {}
    for msg_key in config["message_keys"]:
        key = get_output_key(msg_key)
        paths[msg_key] = {
            "json": output_dir / f"{exp_id}_{key}.json"
        }

    config["paths"] = paths
    return config


