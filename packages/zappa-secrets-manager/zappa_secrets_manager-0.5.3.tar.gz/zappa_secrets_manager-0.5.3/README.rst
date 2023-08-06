# zappa-secrets-manager

A package that will aid in deploying python projects via zappa while using AWS Secrets Manager.  This package makes it easier to develop a project using only a few simple changes in order to swap between development and production

## Available Options

PROJECT_NAME (required) - The name of the project part of the key to look up on AWS Secrets Manager

ENV_PATH (required) - The path to the env file that you want to load when developing

EXTRA_ENVS_TO_SET (optional - defaults to []) - A list of two part tuples detailing any extra environment variables that you want to set

ENV_FILE_NAME (optional - defaults to "development.env") - The name of your local environment file

REGION_NAME (optional - defaults to "eu-west-2") - The region to get the AWS Secrets from

## Usage

Add a call to "load_secrets" somewhere in your project initialisation script, preferably before any project specific settings are initialised.

## Full Django Example
In `<project_name>/__init__.py` add the following.

.. code:: python

    # This should be the full path to your local environment file (excluding the file itself)
    ENV_PATH = '<the full path to your local environment file>'

    # Any extra environment settings you wish to set.  The second element of each tuple will get str formatted
    # with your PROJECT_NAME and the STAGE from zappa in order to create a lookup on AWS Secrets Manager
    EXTRA_ENVS_TO_SET = [('DATABASE_PASSWORD', '{PROJECT_NAME}/{STAGE}/db/{PROJECT_NAME}'),]

    load_secrets(PROJECT_NAME='myproject',
                 ENV_PATH=ENV_PATH,
                 EXTRA_ENVS_TO_SET=EXTRA_ENVS_TO_SET,
                 ENV_FILE_NAME='testing.env',
                 REGION_NAME='us-west-1')

## How it works

Zappa Secrets Manager allows you to easily swap between a production environment on the server with only minimal changes to your local codebase.  By default zappa will fail closed - so you need to actively go out of your way to accidentally get production env variables on your local system.


1) zappa-secrets-manager checks for the existence of a zappa STAGE environment variable.  This will always be there if you deploy with zappa.  If this exists and there is no local "development.env" file then it will use the relevant AWS credentials to obtain the AWS Secrets for anything with a key of 'myproject\<stage>'.  It then loads these secrets into your environment for use in your project.
2) If STAGE is not set OR if there is a local "development.env" file then it will load the contents of that file into your environment for use in your project
3) If neither STAGE or "development.env" exists then the system fails with a RuntimeError

## WARNING

**DO NOT COMMIT YOUR LOCAL DEVELOPMENT.ENV FILE**

## How to structure your AWS Secrets Key Names

Zappa Secrets Manager will by default load any secrets that are stored in <PROJECT_NAME>\<STAGE> on the appropriate REGION_NAME into your environment.

For any values in EXTRA_ENVS_TO_SET you can structure your key names however you want.  Zappa Secrets Manager will string format them to include the zappa STAGE and the PROJECT_NAME variables so you can do dynamic lookups.


## Example

Given an ENV_PATH of "path-to-env-file" PROJECT_NAME of "my_project" and a zappa STAGE of "prod" the following will happen:

1. Check to see if "path-to-env-file/development.env" exists.  If it does then it loads the environment variables out of that.
2. If it doesn't exist then it loads all the secrets on the eu-west-2 region with the secret name "my_project/prod" into your environment.
