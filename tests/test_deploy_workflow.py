from pathlib import Path
import re


def test_deploy_automation_does_not_use_gsutil():
    repo_root = Path(__file__).resolve().parents[1]
    deploy_files = [
        repo_root / ".github/workflows/deploy.yml",
        repo_root / "cloudbuild.yaml",
    ]

    for deploy_file in deploy_files:
        content = deploy_file.read_text(encoding="utf-8")
        executable_lines = [
            line for line in content.splitlines() if not line.lstrip().startswith("#")
        ]
        assert not any(
            re.search(r"\bgsutil\b", line, flags=re.IGNORECASE)
            for line in executable_lines
        )
