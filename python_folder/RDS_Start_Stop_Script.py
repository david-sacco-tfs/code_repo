import sys
import botocore
import boto3

#Tag = 'rds-stop'
#Value = 'stop'

def lambda_handler(event, context):
    rds = boto3.client('rds')
    response = rds.list_tags_for_resource(
        ResourceName = 'arn:aws:rds:us-east-1:198504603100:db:use1-rds-cis-upgradesixtwo-dev-orc-vpc-2'
    )

    for tags in response['TagList']:
        print(tags['Key']," : ",tags['Value'])

    for tags in response['TagList']:
        if tags['Key'] == str(Key) and tags['Value'] == str(Tag):
            status = resp['DBInstanceStatus']
            InstanceID = resp['DBInstanceIdentifier']
            print(InstanceID)
            if status == 'available':
                print("Shutting down %s " % InstanceID)
                client.stop_db_instance(DBInstanceIdentifier = InstanceID)
            else:
                print("The database is " + status + " status!")
