# Clima Tool

The tool displays data contained in EPW files

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Python 3 installed on your machine.

If you do not have Python installed on your machine you can follow [this guide](https://wiki.python.org/moin/BeginnersGuide/Download)

### Installation

This guide is for Mac OSX, Linux or Windows.

1. **Get the source code from the GitHub repository**
```
$ git clone https://github.com/CenterForTheBuiltEnvironment/clima.git
$ cd clima
```
2. **Create a virtual environment using the following command:**

On Linux and MAC ` $ python3 -m venv venv `

On Windows ` py -3 -m venv venv `

3. **Activate the virtualenv:**

On Linux and MAC ` $ . venv/bin/activate `

On Windows ` venv\Scripts\activate `

Your shell prompt will change to show the name of the activated environment.

4. **Install Python dependencies**

The dependencies of the tool are all contained in *requirements.txt*. 
Install them all using:
`$ pip install -r requirements.txt`

6. **Run tool locally**

Now you should be ready to run the tool locally.
`python3 main.py`

Visit http://localhost:8050 in your browser to check it out. 
Note that whenever you want to run the tool, you have to activate the virtualenv first.

[comment]: <> (### Versioning)

[comment]: <> (When you release a new version of the tool you should first use `bumpversion` to update the version of the tool. You can use the following command:)

[comment]: <> (```cmd)

[comment]: <> (bumpversion patch  # alternatively you can use minor or major instead of patch)

[comment]: <> (```)

[comment]: <> (Secondly you should describe the changes in `docs/changelog.md`)

[comment]: <> (gcloud builds submit --tag gcr.io/testbed-310521/clima  --project=testbed-310521)

[comment]: <> (gcloud run deploy --image gcr.io/testbed-310521/clima --platform managed  --project=testbed-310521 --allow-unauthenticated)

## Build with
* [Dash](https://plotly.com/dash/) - Framework for building the web app
* [Plotly Python](https://plotly.com/python/) - Used to create the interactive plots 
