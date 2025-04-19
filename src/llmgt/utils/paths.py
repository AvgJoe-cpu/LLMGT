from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]

# === CONFIG ===

def get_config_dir() -> Path:
    return get_project_root() / "CONFIG"

def get_prompts_config_dir() -> Path:
    return get_config_dir() / "prompts_config"

def get_prompts_config(name: str) -> Path:
    name = Path(name).stem
    return get_project_root() / "CONFIG" / "prompts_config" / f"{name}.json"

def get_experimental_config_path(name: str = "experiments_t1.json") -> Path:
    return get_config_dir() / "experimental_config" / name


# === OUTPUT ===

def get_output_dir() -> Path:
    return get_project_root() / "OUTPUT"

def get_sampled_games_dir() -> Path:
    return get_output_dir() / "SAMPLED_GAMES"

def get_sampled_prompts_dir() -> Path:
    return get_output_dir() / "SAMPLED_PROMPTS"

def get_sampled_games_file(name: str) -> Path:
    return get_sampled_games_dir() / name

def get_sampled_prompts_file(name: str) -> Path:
    return get_sampled_prompts_dir() / name

# === TEMPLATES (inside inference/prompts) ===

def get_template_dir():
    return get_project_root() / "src" / "llmgt" / "inference" / "prompts" / "DA"

def get_cot_dir():
    return get_project_root() / "src" / "llmgt" / "inference" / "prompts" / "COT"


# EXPERIMENTS
def resolve_prompt_file(name: str) -> Path:
    return get_sampled_prompts_dir() / name

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

def get_predictions_dir() -> Path:
    return get_output_dir() / "SAMPLED_PREDS"

def get_cache_dir() -> Path:
    return get_output_dir() / "CACHE"

def get_predictions_subdir(name: str) -> Path:
    return get_predictions_dir() / name
