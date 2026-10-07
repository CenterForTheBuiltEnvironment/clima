from pathlib import Path
import re

import yaml


def _contains_gsutil(value: str) -> bool:
    return bool(re.search(r"\bgsutil\b", value, flags=re.IGNORECASE))


def _iter_command_values(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key in {"run", "script", "entrypoint"} and isinstance(value, str):
                yield value
            elif key == "args":
                if isinstance(value, list):
                    for arg in value:
                        if isinstance(arg, str):
                            yield arg
                elif isinstance(value, str):
                    yield value
            yield from _iter_command_values(value)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_command_values(item)


def test_deploy_automation_does_not_use_gsutil():
    repo_root = Path(__file__).resolve().parents[1]
    for path in [".github/workflows/deploy.yml", "cloudbuild.yaml"]:
        content = (repo_root / path).read_text(encoding="utf-8")
        parsed_yaml = yaml.safe_load(content)
        assert not any(_contains_gsutil(value) for value in _iter_command_values(parsed_yaml))
