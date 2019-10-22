#Quick script to find DBs with a given option group name.
import boto3 as bt
​
#Quick script to go through rds and match optiongroups and/or paramgroups
def get_db():
    client = bt.client('rds')
    response = client.describe_db_instances()
    for db in response['DBInstances']:
        for group in db['OptionGroupMemberships']:
            if(group['OptionGroupName'] == '<whatever you are looking for>'):
                print(db['DBInstanceIdentifier'])
        for param in db['DBParameterGroups']:
            if(param['DBParameterGroupName'] == '<whatever you are looking for>'):
                print(db['DBInstanceIdentifier'])
get_db()