#Objective
#Create a script to loop through cloudwatch alarms, obtain instance ID then check all instance IDs to determine if they still exist
#If they still exist then prompt to remove the associated alarm or auto it (preferrable)

#Added check for status to catch terminated instances that are still hangning around...
import boto3 as bt
import sys
#set client
client = bt.client('cloudwatch')
client2 = bt.client("ec2")
#It will return a nested list/dict.
response = client.describe_alarms()
rep = client2.describe_instances()
#Setup lists to store info.
#emptyAlarm = []
alarmList = [] 
instanceList = []
delList = []

#Go through response to filter down to dimensions then get val from dimensions
def get_instances():
    #This get's each instance
    for it in rep['Reservations']:
        for p in it['Instances']:
            #Adding to list to compare
            if(p['State']['Name'] != 'terminated'):
                instanceList.append(p['InstanceId'])
                #print(p['InstanceId'])

#Function to fetch all alarms and populate alarms list.
def get_alarms():
    #print("Alarm Section\n")
    for i in response['MetricAlarms']:
        if(i['Dimensions'] != [] ):
            for k in i['Dimensions']:
                #print('Value',k['Value'])
                if(k['Name'] == 'InstanceId'):
                    if(k['Value'] not in instanceList):
                        alarmList.append(i['AlarmName'])
     

#Function to delete the alerts that have no active instances.
def del_alerts():
    # Delete alarm
    for alarm in alarmList:
        print("Alarm that should be deleted: {}".format(alarm))
    # for d in delList:
    #     client.delete_alarms(
    #     AlarmNames=[d],
    #     )
    #     print("Deleted: ",d)


def compare():
    try:
        # for inst in alarmList:
        #     #print("Alarm missing an EC2 instance: ",inst)
        #     delList.append(inst)
        if(len(alarmList) != 0):
            del_alerts()
        else:
            print("Nothing to be deleted. Good job!")
    except:
        print("An exception has occurred during comparison:",sys.exc_info())


def lambda_handler(event, context):
    #print("Fetching instances...")
    get_instances()
    #print("Fetching alarms...")
    get_alarms()
    #print("Comparing instances and alarms...")
    compare()
