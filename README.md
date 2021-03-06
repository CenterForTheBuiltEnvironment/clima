# Clima Tool

The tool displays data contained in EPW files. You can access the tool via [this link](https://clima-oiook3g2yq-uc.a.run.app/). Alternatively you can access the Beta version using [this link](https://clima-7sr4nnlw7a-uc.a.run.app).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Python 3 installed on your machine and [pipenv](https://docs.pipenv.org).

* If you do not have Python installed on your machine you can follow [this guide](https://wiki.python.org/moin/BeginnersGuide/Download)
* You can install `pipenv` using the following command `pip install pipenv`.

### Installation

This guide is for Mac OSX, Linux or Windows.

1. **Get the source code from the GitHub repository**
```
$ git clone https://github.com/CenterForTheBuiltEnvironment/clima.git
$ cd clima
```
2. **Create a virtual environment using pipenv and install dependencies:**

``` 
pipenv install --three 
```

3. **Run tool locally**

Now you should be ready to run the tool locally.

```pipenv run python my_project.py```

Visit http://localhost:8080 in your browser to check it out. 
Note that whenever you want to run the tool, you have to activate the virtualenv first.

#### Adding new dependencies
Pipfiles contain information about the dependencies of your project, and supersede the requirements.txt file that is typically used in Python projects.

To install a Python package for your project use the install keyword. For example,

```pipenv install beautifulsoup4```

The package name, together with its version and a list of its own dependencies, can be frozen by updating the Pipfile.lock. This is done using the lock keyword,

```pipenv lock```

#### Managing your development environment

There are usually some Python packages that are only required in your development environment and not in your production environment, such as unit testing packages. Pipenv will let you keep the two environments separate using the --dev flag. For example,

```pipenv install --dev nose2```

#### Generate and update the requirement.txt file

You can update the requirement.txt file with the following command.

```pipenv run pip freeze > requirements.txt```

### Versioning

When you release a new version of the tool you should first use `bumpversion` to update the version of the tool. You can use the following command:

```cmd
bumpversion patch  # alternatively you can use minor or major instead of patch
```

If the above command do not work even if you have committed all the files try with `bumpversion patch --allow-dirty`

Secondly you should describe the changes in `CHANGELOG.md`

### Deploy to Google Cloud Run

I have set-up continuous deployment with GitHub actions. Each time a new version of the code is pushed to master the GitHub Action will deploy the application as long as the commit message will contain the following text `bump version`. I have implemented this to limit the number of deployment we do and to ensure we do not inadvertently deploy an app that is not working. Please refer to the previous section which explains how to change the app version number.

#### Test project
```
gcloud builds submit --tag gcr.io/testbed-310521/clima  --project=testbed-310521

gcloud run deploy clima --image gcr.io/testbed-310521/clima --platform managed  --project=testbed-310521 --allow-unauthenticated --region=us-central1
```

## Built with
* [Dash](https://plotly.com/dash/) - Framework for building the web app
* [Plotly Python](https://plotly.com/python/) - Used to create the interactive plots 
