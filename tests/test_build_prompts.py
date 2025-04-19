from llmgt.prompts.build_prompts import build_prompts_factory
import pytest

DUMMY_CONFIG = {
    "v0": {
        "user_template": "tpl.mako",
        "demo_1shot": [
            {
                "demo_context": {"matrix": [[1, 2], [3, 4]]},
                "assistant_answer_file": "ans1.txt"
            }
        ]
    }
}

@pytest.fixture
def tmp_dirs(tmp_path):
    tpl_dir = tmp_path / "templates"
    tpl_dir.mkdir()
    (tpl_dir / "tpl.mako").write_text("Matrix: ${matrix}")

    cot_dir = tmp_path / "cot"
    cot_dir.mkdir()
    (cot_dir / "ans1.txt").write_text("OK")

    return tpl_dir, cot_dir

def test_build_prompts(tmp_dirs):
    tpl_dir, cot_dir = tmp_dirs
    factory = build_prompts_factory(DUMMY_CONFIG, tpl_dir, cot_dir)

    example = {
        "matrix": [[5, 6], [7, 8]],
        "id": "g1"
    }

    output = factory(example)

    assert output["matrix"] == example["matrix"]
    assert output["id"] == example["id"]

    for key, messages in output.items():
        if not key.startswith("v0_"):
            continue

        assert isinstance(messages, list)
        assert len(messages) >= 2  # at least one user + one assistant + real user

        expected_roles = ["user", "assistant"] * ((len(messages) - 1) // 2) + ["user"]
        actual_roles = [m["role"] for m in messages]
        assert actual_roles == expected_roles[:len(messages)]
        for m in messages:
            assert "content" in m
            assert isinstance(m["content"], str)
            assert m["content"].strip() != ""