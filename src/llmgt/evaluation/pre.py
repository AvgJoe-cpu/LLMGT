import json
import re
from collections import OrderedDict

# --- Custom Exceptions ---
class ParserError(Exception):
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.__str__())

    def __str__(self):
        return f"{self.message}: {self.details}" if self.details else self.message

    def to_dict(self):
        return {
            "error": self.message,
            "details": self.details
        }

    @classmethod
    def wrap(cls, fn):
        def wrapped(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except cls as e:
                return e.to_dict()
            except Exception as e:
                return {
                    "error": "UnhandledException",
                    "details": str(e)
                }
        return wrapped

####-- parsing utils

COMPOUND_PATTERN = re.compile(
    r"```json\s*\n(.*?)\n```"      # 1. strict
    r"|```json\s*(.*?)```"                # 2. semi-strict (inline)
    r"|```\s*\n(.*?)\n```"                # 3. untagged block
    r"|^\s*json\s*\n(.*?\{.*?\})",        # 4. line starting with 'json', then block
    re.DOTALL | re.MULTILINE
)

@ParserError.wrap
def rule_compound_fn(data: str):
    match = COMPOUND_PATTERN.search(data)
    if not match:
        return None

    for group in match.groups():
        if group:
            return group.strip()

    return None

@ParserError.wrap
def load_block_fn(data: str):
    return json.loads(data, object_pairs_hook=lambda pairs: OrderedDict(pairs))

# apply extraction and loading in sequence
def build_parse_fn(output_key: str):
    def parse(example):
        inputs = example[output_key][0]["generated_text"]

        # First stage: extraction
        extracted = rule_compound_fn(inputs)
        if isinstance(extracted, dict) and "error" in extracted:
            return {
                f"parsed_{output_key}": None,
                f"error_{output_key}": json.dumps(extracted),
                f"success_{output_key}": False
            }

        # Second stage: parsing
        parsed = load_block_fn(extracted)
        if isinstance(parsed, dict) and "error" in parsed:
            return {
                f"parsed_{output_key}": None,
                f"error_{output_key}": json.dumps(parsed),
                f"success_{output_key}": False
            }

        # All good!
        return {
            f"parsed_{output_key}": json.dumps(parsed),
            f"error_{output_key}": None,
            f"success_{output_key}": True
        }
    return parse

#####---
