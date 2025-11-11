---
description: >-
  These instructions will get you a copy of the project up and running on your  
  local machine for development and testing purposes.
---

# Run project locally

## Prerequisites

Python 3 installed on your machine and [pipenv](https://docs.pipenv.org).

* If you do not have Python installed on your machine you can follow [this guide](https://wiki.python.org/moin/BeginnersGuide/Download)
* You can install `pipenv` using the following command `pip install pipenv`.

## Installation

This guide is for Mac OSX, Linux, or Windows.

1. **Get the source code from the GitHub repository**

   ```text
   $ git clone https://github.com/CenterForTheBuiltEnvironment/clima.git
   $ cd clima
   ```

2. **Create a virtual environment using pipenv and install dependencies:**

   ```text
    pipenv install --dev
   ```

3.  **Run tool locally**

   Now you should be ready to run the tool locally.

   `pipenv run python main.py`

Visit [http://localhost:8080](http://localhost:8080) in your browser to check it out. Note that whenever you want to run the tool, you have to activate the virtualenv first.

### Adding new dependencies

Pipfiles contain information about the dependencies of your project, and supersede the requirements.txt file that is typically used in Python projects.

To install a Python package for your project use the `install` keyword. For example,

`pipenv install beautifulsoup4`

The package name, together with its version and a list of its own dependencies, can be frozen by updating the Pipfile.lock. This is done using the lock keyword,

`pipenv lock`

### Managing your development environment

There are usually some Python packages that are only required in your development environment and not in your production environment, such as unit testing packages. Pipenv will let you keep the two environments separate using the --dev flag. For example,

`pipenv install --dev nose2`

## Testing

This project runs both Python unit tests, and Cypress end-to-end tests in CI.

To run Python tests locally:
- If you haven't already, install Python dev dependencies.
- Then: `pipenv run python -m pytest`

To run Cypress locally:
- If you haven't already, start the Clima application and confirm that http://localhost:8080/ is up.
- Then: `cd tests/node; npm install; npm run cy:open`

## Versioning

When you release a new version of the tool you should first use `bumpversion` to update the version of the tool. You can use the following command:

```text
bumpversion patch  # alternatively you can use minor or major instead of patch
```

If the above command do not work even if you have committed all the files try with `bumpversion patch --allow-dirty`

Secondly, you should describe the changes in `CHANGELOG.md`

## Deploy to Google Cloud Run

You need to have [gcloud](https://cloud.google.com/sdk/docs/install) installed on your computer. A short guide on how to deploy on Google Cloud Run can be found [here](https://youtu.be/FPFDg5znLTM).

First make sure you that:

* gcloud is up-to-date
* that you are logged in with the right account
* you have updated the Pipfile.lock.

First test the application.

```bash
cd tests
pipenv run pytest --base-url=http://127.0.0.1:8080 -vv --numprocesses 4
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
gcloud run deploy clima-test --image us-central1-docker.pkg.dev/clima-316917/cloud-run-source-deploy/clima:latest --region us-central1 --memory 4Gi --cpu 2 --platform managed --allow-unauthenticated
```

### Deploy test version of the project

```bash
gcloud builds submit --project=clima-316917 --substitutions=_REPO_NAME="clima-test",_PROJ_NAME="clima-316917",_IMG_NAME="test",_GCR="us.gcr.io",_REGION="us-central1",_MEMORY="4Gi",_CPU="2"
```

### Deploy main version of the project

```bash
gcloud builds submit --project=clima-316917 --substitutions=_REPO_NAME="clima",_PROJ_NAME="clima-316917",_IMG_NAME="main",_GCR="us.gcr.io",_REGION="us-central1",_MEMORY="4Gi",_CPU="2"
```