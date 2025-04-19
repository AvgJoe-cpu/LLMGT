from llmgt.prompts.build_prompts import build_prompts_factory
from llmgt.utils import get_project_root, get_data_path, get_stage_path

from datasets import Dataset
import json
from pathlib import Path
from typing import Callable


def load_and_transform_dataset(input_path: Path, prompt_fn: Callable) -> Dataset:
    ds = Dataset.from_json(str(input_path))
    return ds.map(prompt_fn)


def load_prompt_config_and_dirs(
    config_name: str,
    style: str,
    cot_style: str = "COT",
    config_dir: str = "prompt_config"
) -> tuple[dict, Path, Path]:

    config_path = get_data_path(config_dir, config_name)
    if not config_path.exists():
        raise FileNotFoundError(f"Prompt config not found: {config_path}")

    cfg = json.load(open(config_path, encoding="utf-8"))
    return cfg, get_data_path("templates", style), get_data_path("templates", cot_style)


def main():
    config_name = "prompts.json"
    style = "DA"
    cot_style = "cot"
    config_dir = "prompt_config"

    config, template_dir, cot_dir = load_prompt_config_and_dirs(
        config_name=config_name,
        style=style,
        cot_style=cot_style,
        config_dir=config_dir
    )

    build_prompts = build_prompts_factory(config, template_dir, cot_dir)
    input_path = get_stage_path("games", "sampled_games_10_batches_variant.json")
    ds = load_and_transform_dataset(input_path, build_prompts)
    for row in ds:
        print(json.dumps(row, indent=2))
        break


if __name__ == "__main__":
    main()