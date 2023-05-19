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
    pipenv install --three
   ```

3.  **Run tool locally**

   Now you should be ready to run the tool locally.

   `pipenv run python my_project.py`

Visit [http://localhost:8080](http://localhost:8080) in your browser to check it out. Note that whenever you want to run the tool, you have to activate the virtualenv first.

### Adding new dependencies

Pipfiles contain information about the dependencies of your project, and supersede the requirements.txt file that is typically used in Python projects.

To install a Python package for your project use the `install` keyword. For example,

`pipenv install beautifulsoup4`

The package name, together with its version and a list of its own dependencies, can be frozen by updating the Pipfile.lock. This is done using the lock keyword,

`pipenv lock`

Remember also to update the `requirements.txt` file with this command:

`pipenv run pip freeze > requirements.txt`

### Managing your development environment

There are usually some Python packages that are only required in your development environment and not in your production environment, such as unit testing packages. Pipenv will let you keep the two environments separate using the --dev flag. For example,

`pipenv install --dev nose2`

### Generate and update the requirement.txt file

You can update the requirement.txt file with the following command.

`pipenv run pip freeze > requirements.txt`

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
