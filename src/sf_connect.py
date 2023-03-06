from simple_salesforce import Salesforce
import requests
import pandas as pd
from io import StringIO
import json
import boto3
from botocore.exceptions import ClientError
from config import config

def get_secret():

    secret_name = "prod/sForce"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = json.loads(get_secret_value_response['SecretString'])

    print(secret)

    return secret


def sf_connect():

    params = config(section='salesforce')
    print(params)

    """
    secret = get_secret()

    username = params["userName"]
    password = params["password"]
    security_token = params["accessToken"]
    """

    username = params["username"]
    password = params["password"]
    security_token = params["security_token"]
    
    sf = Salesforce(username=username,password=password, security_token=security_token)

    descri=sf.Account.describe()
    print([field['name'] for field in descri['fields']])


if __name__ == '__main__':
    sf_connect()