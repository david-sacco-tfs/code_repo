#Script to run Daily/Weekly to access the instanceLogs folder and remove logs that are older than x days.
# This should be determined from Cloudwatch (age of logs and bucket name)
# Cannot determine from cloudwatch as it does not monitor file ages. Perhaps trigger when new item is made in folder?

#Scan all s3 buckets
# Remove logs in intanceLogs folder that are older than 6months.

#Need to enable the delete part to fully work.

import boto3 as bt 
import time 
from datetime import datetime, timedelta
from time import mktime 
import os 
import logging

logger = logging.getLogger()
today = datetime.today()
today = datetime.strftime(today, '%Y-%m-%d')
today = datetime.strptime(today, '%Y-%m-%d')
#client = bt.client('cloudwatch')
s3client = bt.client('s3')
s3buck = bt.resource('s3')
buckName = []
#Number of days before they can be deleted
log_age_to_keep = 45
log_age_rotated = 183 #approx 6 months
#No duplicates
seen = set(buckName)

#To do delete objects then please uncomment delete section in this function.
#This function deletes the files that have been deemed to old.
def delete_old_logs(path,bucket):
    obj = s3buck.Object(bucket,path)
    print('Mock deleted this item: {} in {}'.format(path, bucket))
    #test = obj.delete()
    # if test:
    #     print('Deleted this item: ', path, 'in ', bucket)

def bucket_check():
    #Get all bucket names
    for buck in s3buck.buckets.all():
            bu = s3buck.Bucket(buck.name)
            #Only interested in buckets which meet the filter.
            for object in bu.objects.filter(Prefix='instanceLogs/'):
                seen.add(object.bucket_name)
    check_date(seen)
    

def check_date(seen,prefix='instanceLogs/'):
    #Iterate through the seen set to get the buckets which have instanceLogs
    for x in seen:
        #List objects in buckets with the given prefix
        folder = s3client.list_objects_v2(Bucket=x, Prefix=prefix, Delimiter='//')
        for t in folder:
            if t == 'Contents':
                for y in folder[t]:
                    #Ignore subdirectory rotated and remove instanceLogs directory from results.
                    #don't want to delete the whole directory!
                    if(('rotated') in y['Key'] or y['Key'] == 'instanceLogs/'):
                        pass
                    else:
                        try:
                            print(os.path.isfile(y['Key']))
                            h = y['LastModified']
                            #Format the time in but in string
                            h = datetime.strftime(h, '%Y-%m-%d')
                            # Basically convert back to datetime object (notice f is replaced with p)
                            h = datetime.strptime(h, '%Y-%m-%d')
                            #Calculate difference in days.
                            diff = abs((today - h).days)
                            #Check to be sure diff is >= 0 (it should not be negative.)
                            assert diff >= 0, 'difference is negative. Not possible. Time travel?'
                            #print("Difference in days: ", abs((today - h).days))
                            try:
                                if(diff > log_age_to_keep):
                                    print(y['Key'])
                                    delete_old_logs(y['Key'],x)
                            except ValueError:
                                print('Seems diff was not defined or is not proper type.')
                            except Exception as e:
                                print("Unable to call delete on provided logs. Attempting to print key. If no key is printed onscreen then log may have been deleted.", y['Key'])
                                print(e.message)
                        except Exception as e:
                            print("Error checking key for instanceLogs.", e.message)
    