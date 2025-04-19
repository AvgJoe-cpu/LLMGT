from mako.lookup import TemplateLookup
import json

def build_prompts_factory(config, template_dir, cot_dir):
    lookup = TemplateLookup(directories=[str(template_dir)])

    def render_prompt(template, context):
        return template.render(**context)

    def load_assistant_answer(answer_file):
        return (cot_dir / answer_file).read_text().strip()

    def build_demo_messages(template, shots):
        messages = []
        for shot in shots:
            user_text = render_prompt(template, shot["demo_context"])
            assistant_text = load_assistant_answer(shot["assistant_answer_file"])
            messages.append({"role": "user", "content": user_text})
            messages.append({"role": "assistant", "content": assistant_text})
        return messages

    def build_prompts(example):
        result = dict(example)
        real_user_context = {"matrix": example["matrix"]}

        for version, config_entry in config.items():
            template = lookup.get_template(config_entry["user_template"])

            for shot_key, demos in config_entry.items():
                if shot_key == "user_template":
                    continue

                demo_messages = build_demo_messages(template, demos)
                real_user_prompt = {
                    "role": "user",
                    "content": render_prompt(template, real_user_context)
                }

                flat_key = f"{version}_{shot_key}"
                result[flat_key] = demo_messages + [real_user_prompt]

        return result

    return build_prompts
