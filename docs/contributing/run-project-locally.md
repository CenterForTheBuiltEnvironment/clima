---
description: >-
  These instructions will get you a copy of the project up and running on your  
  local machine for development and testing purposes.
---

# Run project locally

## Prerequisites

Python 3 should be installed on your machine.

* If you do not have Python installed on your machine you can follow [this guide](https://wiki.python.org/moin/BeginnersGuide/Download)

## Installation

This guide is for Mac OSX, Linux, or Windows.

1. **Get the source code from the GitHub repository**

   ```text
   $ git clone https://github.com/CenterForTheBuiltEnvironment/clima.git
   $ cd clima
   ```

2. **Create a virtual environment and install dependencies:**

   ```text
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3.  **Run tool locally**

   Now you should be ready to run the tool locally.

   `python main.py`

Visit [http://localhost:8080](http://localhost:8080) in your browser to check it out. Note that whenever you want to run the tool, you have to activate the virtualenv first.

### Adding new dependencies

For production dependencies, add them to `requirements.in` and then

```
pip-compile requirements.in
pip install -r requirements.txt
```

For development-only dependencies, add them to `requirements-dev.in` and then

```
pip-compile requirements-dev.in
pip install -r requirements-dev.txt
```

## Testing

This project runs both Python unit tests, and Cypress end-to-end tests in CI.

To run Python tests locally:
- If you haven't already, install Python dev dependencies.
- Then: `python -m pytest`

To run Cypress locally:
- If you haven't already, start the Clima application and confirm that http://localhost:8080/ is up.
- Then: `cd tests/node; npm install; npx run cypress open`

## Versioning

When you release a new version of the tool you should first use `bumpversion` to update the version of the tool. You can use the following command:

```text
bumpversion patch  # alternatively you can use minor or major instead of patch
```

If the above command do not work even if you have committed all the files try with `bumpversion patch --allow-dirty`

Secondly, you should describe the changes in `CHANGELOG.md`

## Deploy to Google Cloud Run

You need to have [gcloud](https://cloud.google.com/sdk/docs/install) installed on your computer. A short guide on how to deploy on Google Cloud Run can be found [here](https://youtu.be/FPFDg5znLTM).

First make sure you that gcloud is up-to-date and that you are logged in with the right account.
```text
gcloud components update
gcloud auth list
```

```text
gcloud builds submit --tag us-docker.pkg.dev/clima-316917/gcr.io/clima  --project=clima-316917

gcloud run deploy clima --image us-docker.pkg.dev/clima-316917/gcr.io/clima --platform managed  --project=clima-316917 --allow-unauthenticated --region=us-central1 --memory=2Gi --concurrency=80 --cpu=2
```

### Test project

```text
gcloud builds submit --tag us-docker.pkg.dev/clima-316917/gcr.io/clima-test  --project=clima-316917

gcloud run deploy clima-test --image us-docker.pkg.dev/clima-316917/gcr.io/clima-test --platform managed  --project=clima-316917 --allow-unauthenticated --region=us-central1 --memory=2Gi --concurrency=80 --cpu=2
```
