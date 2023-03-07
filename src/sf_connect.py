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

    results=sf.query_all(
    """
    Select 
    OwnerId,
    Id,
    CreatedDate,
    LastModifiedDate,
    Name,
    Description,
    X2023_Target_Revenue__c,
    BillingState,
    BillingCountry,
    BillingPostalCode,
    Account_Gameplan__c,
    Account_Status__c,
    Account_Structure__c,
    Client_Category__c,
    CRD_Number__c,
    Date_Opened__c,
    Elevation_cover__c,
    Elevation_Coverage_1__c,
    Elevation_Coverage_1_Asset_Class__c,
    Elevation_Coverage_2__c,
    Elevation_Coverage_2_Asset_Class__c,
    Elevation_Coverage_3__c,
    Elevation_Coverage_3_Asset_Class__c,
    Elevation_Product_Interest__c,
    Is_Account_Closed__c,
    Notes__c,
    Open_to_Trade_Options__c,
    Phone,
    SEC_Number__c,
    Schedule_Research_Calls__c,
    Website
    from Account
    """)
    
    print(type(results))


if __name__ == '__main__':
    sf_connect()