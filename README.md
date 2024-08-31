
# Chinook Postgres Pulumi Example

This repository demonstrates an example implementation using API Foundry. In this example, we will deploy an API that exposes the Chinook database hosted on Postgres, with Pulumi handling the deployment.

Most of the development will be done locally, with the API deployed to a Localstack container running on Docker. The Postgres database will also run in a Docker container.

> [Chinook](https://github.com/lerocha/chinook-database) is a sample database with scripts for Postgres, Oracle, MySQL and other database engines,  It's size an scope make it great for development and testing.  

# Prerequisites

* [Docker](https://www.docker.com) needs to be installed.
* [Pulumi](https://www.pulumi.com) is required for deploying the API.
* Clone the [Localstack Playground](https://github.com/DanRepik/localstack_playground) repository, which provides scripts for setting up a local development environment with Docker, including Localstack and databases running in Docker containers.

# Project Setup

This section guides you through setting up a Pulumi project for an API-Foundry API.

## Create the API-Foundry Project

To begin, create your Pulumi project. If you haven’t logged into Pulumi yet, start by running:

```bash
pulumi login --local
```

Next, set up the Pulumi project using the following command:

```bash
pulumi new aws-python \
  --runtime-options "toolchain=pip,virtualenv=venv" \
  --name "Chinook-API" \
  --description "Chinook API built using API-Foundry" \
  --stack "local" \
  --yes
```

The `template` (`aws-python`) and `runtime-options` must remain as shown. However, you can customize the `name`, `description`, and `stack` values.

## Install Python Packages

Update the `requirements.txt` file to include the necessary packages:

- **api-foundry**: Contains the Pulumi component for building and deploying the API.
- **pulumi-local**: Provides utilities for deploying to Localstack with Pulumi.
- **pytest**: A testing framework.

Here’s the full `requirements.txt`:

```text
pulumi>=3.0.0,<4.0.0
pulumi-aws>=6.0.2,<7.0.0
pulumi-local
api-foundry
pytest
```

Activate the virtual environment and install the required packages using pip:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

You can now test the project deployment with:

```bash
pulumilocal up -y
```

The default template code will create an S3 Bucket. After deployment, verify its existence with:

```bash
AWS_ENDPOINT_URL=https://localhost.localstack.cloud:4566 aws s3 ls
```

Finally, clean up with:

```bash
pulumilocal down -y
```

## localtools.sh (optional)

Next let's setup localtools.sh this is a script that streamlines development by providing a set of alias's for common operations.

'localtools.sh' starts the Python virual environment and sets alias's to bring deployments up and down.  Additionally it includes operations to management the Localstack and Postgres development infrastructure.

```bash
source venv/bin/activate

alias up="pulumi up --yes --stack local"
alias down="pulumi destroy --yes --stack local"

# import playground commands
source "~/workspace/localstack_playground/devtools.sh"

alias infra_up="playground_postgres; ./install_secrets.py"
alias infra_down="playground_down"
alias infra_reset="playground_reset"
```


# Installation

1. Install the Python modules.  The example uses Pipenv to manage python virtual environments and resources.  To install those resources run;

```bash
pipenv install
```

2. The devtools.sh file contains alias and settings that streamline develop activaties.  To initialize a terminal environment with the devtools.sh run;

```bash
source devtools.sh
```

create_secret_if_not_exists(
    "postgres/chinook",
    json.dumps(
        {
            "engine": "postgres",
            "dbname": "chinook_auto_increment",
            "username": "chinook_user",
            "password": "chinook_password",
            "host": "postgres_db",
        }
    ),
)

# Developing the Chinook API

## Implement the API Specfication

## Configure the Database Connection

## Create the API


## AWS Configuration

In order to make deployments valid AWS credentials must be provided. The devtools.sh script sets AWS_PROFILE to 'localstack' by default however this can be overridden it needed.

To deploy to Localstack you will need to add a 'localstack' profile to you AWS configuration.  To do that add the following to the '~/.aws/credentials' file;

```
[localstack]
aws_access_key_id = test
aws_secret_access_key = test
```

And to your '~/.aws/config' file add the following profile;

```
[profile localstack]
region = us-east-1
endpoint_url = http://localhost.localstack.cloud:4566
```

## Dev Playground

The Dev Playground is a docker compose file that sets up both Localstack and a collection of databases running in Docker.  The playground provides a local environment where API-Foundry deployments can be made.

The Dev Playground runs with Postgres, Oracle, and MySQL databases and they are initialized with the Chinook open source database.

The playground must be running when making local deployments and using the Chinook example databases.

**Start Playground**

To start the playground run;

```bash
playground_up
```

Individual databases can be started with;

```bash
playground_postgres
playground_oracle
playground_mysql
```


**Stop the Playground**

To stop the playground run;

```bash
playground_down
```

**Reset the Playground**

Reset allows restoring the databases back to their original state.

```bash
playground_reset
```

Resetting the database shuts down all playground containers and removes the database volumes.

# Running an Example Deployment

**Deploy to the Playground**

To make a deployment run;

```bash
up
```

**Destory a Deployment**

To destroy a deployment run;

```bash
down
```
