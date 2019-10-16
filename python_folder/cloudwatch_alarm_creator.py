import json
import boto3 as bt
import sys
import logging
import os

#set client
client = bt.client('cloudwatch')
client2 = bt.client('ec2')
#It will return a nested list/dict.
response = client.describe_alarms()
rep = client2.describe_instances()
#Setup lists to store info.
alarmList = [] 
instanceList = []
delList = []
logger = logging.getLogger()

def lambda_handler(event, context):
    setLogLevel(os.environ['logLevel'])
    #Set logging
    logger.debug('logLevel: '+os.environ['logLevel'])
    logger.info('Checking cloudwatch.')
    get_instances()
    get_alarms()
    compare()
    
    message = 'Cloudwatch Alarm Creation Complete, yeet'

    return {
        'message':str(message)
        }

#Go through response to filter down to dimensions then get val from dimensions
def get_instances():
    #This get's each instance
    for it in rep['Reservations']:
        for p in it['Instances']:
            #Adding to list to compare
            if(p['State']['Name'] != 'pending'):
                instanceList.append(p['InstanceId'])
        
#Function to delete the alerts that have no active instances.
def create_alert_1():
    # Delete alarm
    for alarm in alarmList:
        logger.info("Alarm that will be created: {}".format(alarm))
    # for d in instanceList:
    #     client.put_metric_alarm(
    #     AlarmNames='',
    #     ComparisonOperator='',
    #     EvaluationPeriods=3,
    #     MetricName='',
    #     Namespace='AWS/EC2',
    #     Period=15,
    #     Statistic='',
    #     Threshold=<float>,
    #     ActionsEnabled=false,
    #     AlarmDescription='',
    #
    #     )
    #     print("Deleted: ",d)


def compare():
    assert len(alarmList) >=0, logger.warning('AlarmList is list than 0. How?')
    try:
        if(len(alarmList) != 0):
            del_alerts()
        else:
            logger.info("Nothing to be deleted. Good job!")
    except:
        logger.error("An exception has occurred during comparison:",sys.exc_info())




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