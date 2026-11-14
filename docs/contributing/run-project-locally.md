---
description: >-
  These instructions will get you a copy of the project up and running on your  
  local machine for development and testing purposes.
---

# Run project locally

## Prerequisites

[uv](https://docs.astral.sh/uv/) installed on your machine. You can install it by following the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

* uv reads the Python version from `.python-version` (3.11) and downloads it if it is not already installed, so you do not need to install Python separately.

## Installation

This guide is for Mac OSX, Linux, or Windows.

1. **Get the source code from the GitHub repository**

   ```text
   $ git clone https://github.com/CenterForTheBuiltEnvironment/clima.git
   $ cd clima
   ```

2. **Create a virtual environment and install dependencies:**

   ```text
    uv sync
   ```

3.  **Run tool locally**

   Now you should be ready to run the tool locally.

   `uv run python main.py`

Visit [http://localhost:8080](http://localhost:8080) in your browser to check it out. `uv run` uses the project's virtual environment, so you do not need to activate it first.

### Adding new dependencies

`pyproject.toml` lists the dependencies of the project, and `uv.lock` records the exact version of every package that gets installed.

To add a Python package to the project use the `add` command. For example,

`uv add beautifulsoup4`

`uv add` updates both `pyproject.toml` and `uv.lock`. If you edit `pyproject.toml` by hand, update the lock file with

`uv lock`

### Managing your development environment

There are usually some Python packages that are only required in your development environment and not in your production environment, such as unit testing packages. uv keeps them in a separate `dev` dependency group using the --dev flag. For example,

`uv add --dev nose2`

## Testing

The tests are end-to-end tests written with pytest and [Playwright](https://playwright.dev/python/). CI runs them on every push and pull request to `development`.

To run them locally:
- Install the browser Playwright uses (only needed once): `uv run playwright install chromium`
- Start the Clima application with `uv run python main.py` and confirm that http://localhost:8080/ is up.
- In a second terminal, run the tests:

```bash
cd tests
uv run pytest --base-url=http://127.0.0.1:8080 -vv --numprocesses 4
```

## Versioning

When you release a new version of the tool you should first use `bump2version` to update the version of the tool. You can use the following command:

```text
uv run bump2version patch  # alternatively you can use minor or major instead of patch
```

`bump2version` updates the version in `pyproject.toml`, `uv.lock`, `pages/lib/layout.py` and `assets/manifest.json`, then commits the change and tags it. The settings are in `.bumpversion.cfg`.

If the above command does not work even if you have committed all the files try with `uv run bump2version patch --allow-dirty`

Secondly, you should describe the changes in `docs/version/changelog.md`

## Deploy to Google Cloud Run

You need to have [gcloud](https://cloud.google.com/sdk/docs/install) installed on your computer. A short guide on how to deploy on Google Cloud Run can be found [here](https://youtu.be/FPFDg5znLTM).

First make sure you that:

* gcloud is up-to-date
* that you are logged in with the right account
* you have updated `uv.lock` (`uv lock`) and committed it.

First test the application.

```bash
cd tests
uv run pytest --base-url=http://127.0.0.1:8080 -vv --numprocesses 4
```

### Deploy test version manually using gcloud and docker locally - quicker and great to test small changes

```bash
gcloud components update --quiet
gcloud auth login  # or gcloud config set account ACCOUNT
gcloud config set project clima-316917
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet
docker buildx build --platform linux/amd64 -t us-central1-docker.pkg.dev/clima-316917/cloud-run-source-deploy/clima:latest .

# run locally to test
docker run --platform linux/amd64 --rm -p 8080:8080 us-central1-docker.pkg.dev/clima-316917/cloud-run-source-deploy/clima:latest
# Run detached, give a name, set env vars, and print logs
docker run -d --platform linux/amd64 --name clima-test -p 8080:8080 -e ENV=dev us-central1-docker.pkg.dev/clima-316917/cloud-run-source-deploy/clima:latest
docker logs -f clima-test

# if everything is ok push to google container registry
docker push us-central1-docker.pkg.dev/clima-316917/cloud-run-source-deploy/clima:latest
gcloud run deploy clima-test --image us-central1-docker.pkg.dev/clima-316917/cloud-run-source-deploy/clima:latest --region us-central1 --memory 4Gi --cpu 2 --platform managed --allow-unauthenticated --tag "v0-10-2"

# you can then deploy the main version changing the name and tag
gcloud run deploy clima --image us-central1-docker.pkg.dev/clima-316917/cloud-run-source-deploy/clima:latest --region us-central1 --memory 4Gi --cpu 2 --platform managed --allow-unauthenticated --tag "v0-10-2"
```

### Deploy test version of the project

```bash
gcloud builds submit --project=clima-316917 --substitutions=_REPO_NAME="clima-test",_PROJ_NAME="clima-316917",_IMG_NAME="test",_GCR="us.gcr.io",_REGION="us-central1",_MEMORY="4Gi",_CPU="2"
```

### Deploy main version of the project

```bash
gcloud builds submit --project=clima-316917 --substitutions=_REPO_NAME="clima",_PROJ_NAME="clima-316917",_IMG_NAME="main",_GCR="us.gcr.io",_REGION="us-central1",_MEMORY="4Gi",_CPU="2"
```