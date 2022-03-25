# CDKTF GCP Functions Trial

Trial on deploying simple Google Cloud Functions Python application with CDKTF on GCP.

### Requirements

- Python 3.8
- [GCP Functions Framework](https://github.com/GoogleCloudPlatform/functions-framework-python)
- [CDKTF](https://www.terraform.io/docs/cdktf/index.html)
- [gcloud CLI](https://cloud.google.com/sdk/docs/install)

### Installation

Install `CDKTF` and `gcloud CLI` from links above.

Ensure Cloud Build API is enabled in Google project

### Clone Project

```sh
git clone https://github.com/taiyeoguns/cdktf-gcp-cloud-functions-trial.git
```

and then change to directory

```sh
cd cdktf-gcp-cloud-functions-trial
```

### Create and activate virtual environment

```sh
python -m venv venv
```

```sh
source venv/bin/activate
```


### Set up gcloud

If gcloud not already set up, open a command prompt, enter:

```sh
gcloud init
```

and follow the instructions.

### Install Requirements

```sh
pip install -r requirements.txt
```

### Get terraform modules
```sh
cd infrastructure
cdktf get
```

### Run locally

```sh
cd application
functions-framework --target=hello_http
```

Server should be started at `http://localhost:8080`

### GCP Deployment

To spin up resources, enter:

```sh
cd infrastructure
cdktf deploy
```

to auto approve, use:

```sh
cd infrastructure
cdktf deploy --auto-approve
```

If successful, deployed application url should be available from the `function_url` output in the console, e.g. `https://us-east1-positive-cacao-243516.cloudfunctions.net/cf-d1d0b561`

Endpoint can be tested with `https://us-east1-positive-cacao-243516.cloudfunctions.net/cf-d1d0b561`

To tear down resources, use:

```sh
cd infrastructure
cdktf destroy
```

to auto-approve, use:

```sh
cd infrastructure
cdktf destroy --auto-approve
```

###  Project layout

This project structure combines a CDKTF application and a GCP Functions application. These correspond to the `infrastructure` and `application` directories respectively.  To run any CDKTF commands, ensure you're in the `infrastructure` directory, and to run any gcloud Functions framework commands ensure you're in the `application` directory.
