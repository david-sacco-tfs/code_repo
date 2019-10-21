import json
import boto3 as bt
import sys
import logging
import os
from collections import defaultdict

# Variables
evaluationPeriods=5
CPUThreshhold=90
DiskThreshhold=90
MemoryThreshhold=98
SwapThreshhold=5
period=60
ACCOUNT_ID = context.invoked_function_arn.split(":")[4]
sns_Topic = ''
complete = False

# Set client
client = bt.client('cloudwatch')
client2 = bt.client('ec2')
client3 = bt.client('sns', region=AWS_REGION)

# It will return a nested list/dict.
rep = client2.describe_instances()
coreit_sns = client3.list_topics()
# Setup variables to store info.
ec2info = defaultdict()
logger = logging.getLogger()
instanceList = []
subscriptionList = sns.list_subscriptions()
allSubscriptionsList = []
allSubscriptionsList.extend(subscriptionList['Subscriptions'])

##############################################################################

def lambda_handler(event, context):
    setLogLevel(os.environ['logLevel'])
    logger.debug('logLevel: '+os.environ['logLevel']) #Set Logging
    logger.info('Checking cloudwatch.')
    get_coreit_sns_topic()
    get_pending_instances()
    create_alerts()
    
    message = 'Cloudwatch Alarm Creation Complete, yeet'

    return {
        'message':str(message)
    }

##############################################################################


# Go through SNS to filter out CoreIT topic ONLY!!
def get_coreit_sns_topic():
    while (not complete):
        if ('NextToken' in subscriptionList ) :
            token = subscriptionList['NextToken']
            subscriptionList = sns.list_subscriptions(NextToken=token)
            allSubscriptionsList.extend(subscriptionList['Subscriptions'])
        else :
            complete = True

    for subscription in allSubscriptionsList:
        #print (subscription)
        if 'CoreIT' in subscription['SubscriptionArn']:
            snsTopic = subscription['TopicArn']
            break

    print(snsTopic)

# Go through response to filter down to dimensions then get val from dimensions
def get_pending_instances():
    #This get's each instance
    for it in rep['Reservations']:
        for p in it['Instances']:
            #Adding to list to compare
            if(p['State']['Name'] == 'pending'):
                instanceList.append(p['InstanceId'])
        
# Function to create alerts for instances that are in 'pending'.
def create_alerts():
    for d in instanceList:
        ##### Swap Threshold Alarm Creation ####
        client.put_metric_alarm(
            AlarmNames='High-Swap-Utilization-' + (AWS_REGION) + '-' + (ACCOUNT_ID) + '-' + ,
            AlarmActions=sns_Topic,
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=evaluationPeriods,
            MetricName='SwapUtilization',
            Namespace='System/Linux',
            Period=15,
            Statistic='Average',
            Threshold=SwapThreshhold,
            TreatMissingData='Missing'
            Unit='Percent',
            ActionsEnabled=false,
            AlarmDescription=('Alarm when Swap exceeds' + SwapThreshold + 'percent over' + evaluationPeriods + 'minutes.')
        )
        print("Created: ", d)   

def setLogLevel(logLevel):
    if logLevel.lower() == 'debug':
        logger.setLevel(logging.DEBUG)

    if logLevel.lower() == 'info':
        logger.setLevel(logging.INFO)

    if logLevel.lower() == 'warning':
        logger.setLevel(logging.WARNING)

    if logLevel.lower() == 'error':
        logger.setLevel(logging.ERROR)

    if logLevel.lower() == 'critical':
        logger.setLevel(logging.CRITICAL)

    if logger.getEffectiveLevel() == 0:
        logger.setLevel(logging.DEBUG)