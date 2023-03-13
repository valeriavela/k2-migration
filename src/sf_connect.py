from simple_salesforce import Salesforce
import requests
import pandas as pd
from io import StringIO
import json
import boto3
from botocore.exceptions import ClientError
from config import config
from datetime import datetime

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
    records = [dict(salesforce_account_owner=rec['OwnerId'],
                salesforce_account_id=rec['Id'],
                salesforce_created=rec['CreatedDate'],
                salesforce_last_modified=rec['LastModifiedDate'],
                name=rec['Name'],
                description=rec['Description'],
                target_revenue_2023=rec['X2023_Target_Revenue__c'],
                billing_state=rec['BillingState'],
                billing_country=rec['BillingCountry'],
                billing_zip_code=rec['BillingPostalCode'],
                account_gameplan=rec['Account_Gameplan__c'],
                account_status=rec['Account_Status__c'],
                account_structure=rec['Account_Structure__c'],
                client_category=rec['Client_Category__c'],
                crd_number=rec['CRD_Number__c'],
                date_opened=rec['Date_Opened__c'],
                elevation_coverage=rec['Elevation_cover__c'],
                elevation_coverage_1=rec['Elevation_Coverage_1__c'],
                elevation_coverage_1_asset_class=rec['Elevation_Coverage_1_Asset_Class__c'],
                elevation_coverage_2=rec['Elevation_Coverage_2__c'],
                elevation_coverage_2_asset_class=rec['Elevation_Coverage_2_Asset_Class__c'],
                elevation_coverage_3=rec['Elevation_Coverage_3__c'],
                elevation_coverage_3_asset_class=rec['Elevation_Coverage_3_Asset_Class__c'],
                elevation_product_interest=rec['Elevation_Product_Interest__c'],
                is_account_closed=rec['Is_Account_Closed__c'],
                notes=rec['Notes__c'],
                open_to_trade_options=rec['Open_to_Trade_Options__c'],
                phone=rec['Phone'],
                sec_number=rec['SEC_Number__c'],
                scheduled_research_calls=rec['Schedule_Research_Calls__c'],
                website=rec['Website']) 
                for rec in results['records']]
    
    df=pd.DataFrame(records)
    # df.to_csv("/Users/valeriavela/Downloads/sf_results.csv")

    now = datetime.now()

    bucket = 'k2-sf-clients' # already created on S3
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    file_name = 'clients_' + now.strftime("%m%d%YT%H:%M:%S") + '.csv'
    s3_resource.Object(bucket, file_name).put(Body=csv_buffer.getvalue())



if __name__ == '__main__':
    sf_connect()