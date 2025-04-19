from datasets import Dataset
import argparse
import json
from .build_prompts import build_prompts_factory
from llmgt.utils.paths import get_sampled_games_file, get_sampled_prompts_dir
from llmgt.utils.paths import *


def main():
    parser = argparse.ArgumentParser(description="Build and export prompt-structured data.")
    parser.add_argument("file", type=str, nargs="?", default="sampled_games_10_batches_variant.json")
    parser.add_argument("--config", type=str, default="prompts_config.json")
    parser.add_argument("--style", type=str, default="DA", help="Prompt style subfolder (e.g. DA or COT)")

    args = parser.parse_args()

    input_path = get_sampled_games_file(args.file)
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    config_path = get_prompts_config(args.config)
    with open(config_path, "r", encoding="utf-8") as f:
        prompt_config = json.load(f)

    # Paths based on style
    template_dir = get_project_root() / "src" / "llmgt" / "inference" / "prompts" / args.style
    cot_dir = get_project_root() / "src" / "llmgt" / "inference" / "prompts" / "COT"

    prompt_fn = build_prompts_factory(prompt_config, template_dir, cot_dir)

    ds = Dataset.from_json(str(input_path))
    ds = ds.map(prompt_fn)

    output_dir = get_sampled_prompts_dir()
    output_dir.mkdir(parents=True, exist_ok=True)

    out_name = f"prompts_from_{input_path.stem}.json"
    output_path = output_dir / out_name

    with open(output_path, "w") as f:
        json.dump(ds.to_list(), f, indent=2)

    print(f"Prompts exported to: {output_path}")

if __name__ == "__main__":
    main()