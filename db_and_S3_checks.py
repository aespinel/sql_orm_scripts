"""
1. The purpose of the code is to perform image checks in database and S3
2. Addresses the purpose by filtering out and storing person ids on state names in a list and then perform checks walking through the directory on the person ids list and S3 simultaneously.
3. Inputs - directory (in which directory walk must take place) and state ids
4. Outputs - three different csv files, contains person ids

Note:
1.Make sure to change the system accordingly to dg folder
2.CSV files will be generated in the current directory
"""
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import csv, os, sys
sys.path.append(r'C:\Users\chandu\Documents\dg')
from django.core.management import setup_environ
import settings
setup_environ(settings)

from dashboard.models import Person

ACCESS_KEY = '01GE4NJEXRFQTBCFG782'
SECRET_KEY = 'bK8gt4siHBryH/cRagSMtcDPwNbfB0l2E/KXVhYy'
BUCKET_NAME = 'dg_farmerbook'

con = S3Connection(ACCESS_KEY, SECRET_KEY)
bucket = con.get_bucket(BUCKET_NAME)
#state ids
state_ids = [10000000000002, 10000000000003]
not_uploaded=[]
uploaded =[]
not_in_db = []
person_ids=Person.objects.filter(village__block__district__state_id__in= state_ids).values_list('id', flat=True)
#get files by walking though below mentioned directory
for root, dirs, files in os.walk(r'G:\farmerbook_backup_pics\JOB'):
	for file_name in files:
		name_split = os.path.splitext(file_name)
		id = name_split[0] #name of the image after removing extension
		#id.isdigit() checks for weather the id is valid digit
		if id.isdigit():
			if int(id) in person_ids:
				if bucket.get_key('2/' + file_name):
					uploaded.append(id)
				else:
					not_uploaded.append(id)
			else:
				not_in_db.append(id)
		else:
			not_in_db.append(id)

#For generating CSV file for invalid names
csv_file = open('invalid_names.csv',"wb")			
wrtr = csv.writer(csv_file, delimiter=',',)
for id in not_in_db:
	wrtr.writerow([id])
csv_file.close()

#For generating CSV file for not uploaded but in database
csv_file1 = open('not_uploaded.csv',"wb")			
wrtr1 = csv.writer(csv_file1, delimiter=',',)
for id in not_uploaded:
	wrtr1.writerow([id])
csv_file1.close()

#For generating CSV file for uploaded
csv_file2 = open('uploaded.csv',"wb")			
wrtr2 = csv.writer(csv_file2, delimiter=',',)
for id in uploaded:
	wrtr2.writerow([id])
csv_file2.close()

print "uploaded"+'  '+str(len(uploaded))
print "not uploaded(but in db)"+'  '+str(len(not_uploaded))
print "not found in DB"+'  '+str(len(not_in_db))