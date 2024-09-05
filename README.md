
# Chinook Postgres Pulumi Example

This repository demonstrates an example implementation using API Foundry. In this example, we will deploy an API that exposes the Chinook database hosted on Postgres, with Pulumi handling the deployment.

Most of the development will be done locally, with the API deployed to a Localstack container running on Docker. The Postgres database will also run in a Docker container.

> [Chinook](https://github.com/lerocha/chinook-database) is a sample database with scripts for Postgres, Oracle, MySQL and other database engines,  It's size an scope make it great for development and testing.  

# Prerequisites

* [Docker](https://www.docker.com) needs to be installed.
* [Pulumi](https://www.pulumi.com) is required for deploying the API.

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
- **localstack-playground** Localstack Playground is a Docker Compose setup with LocalStack and databases (Postgres, Oracle, MySQL) in containers, enabling local development and testing of AWS apps with RDBMS data.
- **pytest**: A testing framework.
- **requests**: Utilities for making HTTP requests.

Here’s the full `requirements.txt`:

```text
pulumi>=3.0.0,<4.0.0
pulumi-aws>=6.0.2,<7.0.0
pulumi-local
localstack-playground
api-foundry
pytest
requests
```

Activate the virtual environment and install the required packages using pip:

```bash
python -m venv venv
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

Next let's setup localtools.sh this is a script that streamlines development by providing a set of alias's for common command line operations.  This file optional and just provides shortcuts.

'localtools.sh' starts the Python virual environment and sets alias's to bring deployments up and down.  Additionally it includes alias's to management the Localstack and Postgres development infrastructure.

```bash
# devtools.sh

# api operations
alias up="pulumilocal up --yes --stack local"
alias down="pulumilocal destroy --yes --stack local"

# playground operations
alias infra_up="playground postgres; postgres_secret"
alias infra_down="playground down"
alias infra_reset="playground reset"

```

Install the tools using;


```bash
source devtools.sh
```

# Implementing the Chinook API

To implement an API using API-Foundry, you need three key components:

1. **API Specification:** Defines the structure and behavior of your API.
2. **AWS Secret:** Contains the database connection configuration.
3. **Deployment Code:** Combines the API specification and AWS secret as a Pulumi component for deployment.

## Implement the API Specification

The first step in developing an API with API-Foundry is to create the API specification document in the OpenAPI 3.0 format. In this document, you'll need to:

* Create a corresponding component schema object for each database table you want to expose in the API.
* Define any additional SQL queries that should be exposed as services within the specification's path object.

> For comprehensive details on building API specifications, please refer to: [Documentation Link](> For comprehensive details on building API specifications, please refer to: [Building an API Definition](https://github.com/DanRepik/api_foundry?tab=readme-ov-file#building-an-api-definition)

To streamline the process, the API-Foundry package includes a script `postgres_to_openapi` that generates a starter specification based on your database connection parameters.  You can modify the result of this script to build your API.

> For complete information on using this utility see: [PostgreSQL Database Schemas](https://github.com/DanRepik/api_foundry?tab=readme-ov-file#postgresql-database-schemas) in the API-Foundry documentation.

```bash
# Needed to access the database in the scope of 
# the utility
pip install psycopg2-binary

# generate and save the API specification
postgres_to_openapi --host localhost \
  --database chinook_auto_increment \
  --user chinook_user \
  --password chinook_password \
  --schema public \
  --output chinook_api.yaml
```

After running the `postgres_to_openapi` utility there should be a `chinook_api.yaml` file containing the a  best guess approximation of the API specification.  There's serval modifications let's make;

First let's shorten the database name.  The Chinook repository offers multiple flavors of the database and this document is tried to one of them.  We can make that more generic by changing all occurences where the `x-af-database` attribute is set to `chinook_auto_increment` to `chinook`.

Additionally the `postgres_to_openapi' utility can not recognize concurrency control columns.  These columns, like a last updated timestamp are used to avoid different clients from overwritting changes made by other clients.  Those will have to added. 

For example the component schema `invoice` object has a `last_updated` property for this purpose.  We need to identify this property by adding the attribute;

```yaml
      x-af-concurrency-control: last_updated
```


By completing these steps, you've established the core of your API-Foundry implementation. The OpenAPI 3.0 specification document defines your API's interaction with the database. With the specification in place, you’re now set to configure deploy your API.


## Configure the Database Connection

For API-Foundry deployments, the Lambda service relies on an AWS secret to retrieve the database connection details. In production, these secrets are usually managed by a system or database administrator. 

However, during Localstack development, you need to manage these secrets locally. API-Foundry provides the `install_secret` script to simplify this process. This script safely installs the secret only if it doesn’t already exist, so you can run it multiple times without issue.

```bash
install_secret \
  --secret-name "postgres/chinook" \
  --engine postgres \
  --host postgres_db \  # docker network host name
  --database chinook_auto_increment \
  --user chinook_user \
  --password chinook_password \
  --schema public
```

When resetting the Localstack playground this secret will be removed, and will need to be reinstalled. To streamline this process, you can include these commands in your `devtools.sh` file:

```bash
# devtools.sh

# api operations
# devtools.sh

# api operations
alias up="pulumilocal up --yes --stack local"
alias down="pulumilocal destroy --yes --stack local"

alias postgres_secret="install_secret --secret-name \"postgres/chinook\" \
  --engine postgres \
  --host postgres_db \
  --database chinook_auto_increment \
  --user chinook_user \
  --password chinook_password \
  --schema public"

# playground operations
alias infra_up="playground postgres; postgres_secret"
alias infra_down="playground down"
alias infra_reset="playground reset"
```

This setup ensures that your infrastructure and secrets are configured correctly and efficiently each time you work with your local environment.

## Create the API

With the API specification completed and the database connection secret configured, the next step is to deploy the API using Pulumi.

You define the `APIFoundry` component in your Pulumi code, typically within the `__main__.py` file. The `APIFoundry` component is a Pulumi `ComponentResource`, so it should be handled like any other component.

There are two key properties to set in the deployment:

* **api_spec**: The file path to the API specification created earlier.
* **secrets**: A JSON mapping of database names to their corresponding secret names. Ensure all databases specified with the `x-af-database` attribute in the API specification are included in this map to correctly associate resources with database connections.

> When deploying to AWS an connecting to RDS databases a VPC configuration will also be required.

Below is the deployment code for the Chinook API:

```python
# __main__.py
import json
from api_foundry.iac.pulumi.api_foundry import APIFoundry

api_foundry = APIFoundry(
    "chinook_postgres",
    props={
        "api_spec": "./chinook_api.yaml",
        "secrets": json.dumps({"chinook": "postgres/chinook"}),
    },
)
```

With the `APIFoundry` component defined, you can now deploy to Localstack using the `up` ('pulumilocal up -y') command.

> Complete documentation on implementing API specifications can be found at [Building An API Definition](https://github.com/DanRepik/api_foundry?tab=readme-ov-file#building-an-api-definition)

## Deploy the API to Localstack

With `devtools.sh` sourced in your terminal, you can manage the Localstack environment using these commands:

- **infra_up**: Starts the Localstack and Postgres containers, and installs the Chinook database secret.
- **infra_reset**: Removes the containers and associated data volumes, along with all resources deployed to Localstack, including secrets.
- **infra_down**: Stops the containers but keeps the data volumes intact.

For handling deployments, the following commands are available:

- **up**: Deploys the API, and can be run multiple times to update the deployment.
- **down**: Removes the deployment.

The typical development workflow is:

1. Start the infrastructure with `infra_up`.
2. Deploy and iterate with `up`.
3. Reset the environment as needed using `infra_reset`.

Once the deployment is complete the API can excerised using curl.  For Localstack you will need to build the URL using the following;

```bash
http://{GATEWAY_API}.execute-api.localhost.localstack.cloud:4566/{api_name}"
```

Where;

* gateway_api is an output by the Pulumi deployment.
* api_name is the name of the Pulumi APIFoundry component.


For example;

```bash
export GATEWAY_API=y8w7zajvlp
export API_NAME=chinook_postgres
export GATEWAY_URL=http://${GATEWAY_API}.execute-api.localhost.localstack.cloud:4566/${API_NAME}
```


## Sending a Request

Once 
