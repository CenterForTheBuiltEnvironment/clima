from pathlib import Path


def test_deploy_automation_does_not_use_gsutil():
    repo_root = Path(__file__).resolve().parents[1]
    deploy_files = [
        repo_root / ".github/workflows/deploy.yml",
        repo_root / "cloudbuild.yaml",
    ]

    for deploy_file in deploy_files:
        content = deploy_file.read_text(encoding="utf-8").lower()
        assert "gsutil" not in content
