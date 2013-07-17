"""
1. The purpose of the code is to generate random adoptions in some villages among some vidoes
2. Addresses the purpose by filter the data, from DB, accordingly and generating a dictionary with village name as it key and list of the adoptions as its values. Then randomize them, if number of adoptions are more than specifed number, and writes to csv file with village name as its name.
3. Inputs - district name (dist_name),
			list of village ids in that district (ids),
			list of videos in which adoptions data needed (vds),
			number of random data needed (random_data_needed)
4. Outputs csv file named after village name. 
	CSV file contains village name, date of adoption, person name, group name, video title, village id, adoption id, person id and video id

Note:
1.Code cannot overwrite or generate csv files if file already exists in the directory
2.Make sure to change the system accordingly to dg folder
"""
import csv, os, site, sys
sys.path.append(r'C:\Users\chandu\Documents\dg')
from django.core.management import setup_environ
import settings
setup_environ(settings)
from dashboard.models import PersonAdoptPractice
from random import choice
#village ids
ids = [10000000000388, 10000000019865, 10000000000385, 10000000000501, 10000000000305, 10000000000505,10000000000537, 10000000019984, 10000000020719, 10000000020591]
#video ids
vds = [10000000021093, 10000000021096, 10000000021146]
dist_name = "keonjhar"
pap = PersonAdoptPractice.objects.filter(person__village__block__district__district_name=dist_name).filter(person__village__id__in = ids).filter(video__in=vds).prefetch_related('person','person__village','person__village__block','person__village__block__district','person__group','video')
random_data_needed = 10
dict={}
#pap contains list of all adoptions from the villages, among the videos, that are mentioned in ids and vds respectively, in dist_name (keonjhar)
#The following loop generates a dictionary with village names as keys and list of all adoptions in that village among those videos mentioned above
for obj in pap:
	if obj.person.village.village_name in dict:
		(dict[obj.person.village.village_name]).append(obj)
	else:
		dict[obj.person.village.village_name] = [obj]

#The following loop generates the 10 random adoptions and write into the csv file with village name as its name, if number of adoptions are more than 10
for key in dict:
	file = open(key,"wb")			
	foo = dict[key]
	if len(foo)>random_data_needed:
		for i in range(0,random_data_needed):
				obj = choice(foo)
				list = [obj.person.village.village_name, obj.date_of_adoption, obj.person.person_name, obj.person.group.group_name, obj.video.title,obj.person.village.id, obj.id, obj.person.id, obj.video.id]
				wrtr = csv.writer(file, delimiter=',')
				wrtr.writerow(list)
	else:
		for obj in foo:
			list = [obj.person.village.village_name, obj.date_of_adoption, obj.person.person_name, obj.person.group.group_name, obj.video.title,obj.person.village.id, obj.id, obj.person.id, obj.video.id]
			wrtr = csv.writer(file, delimiter=',')
			wrtr.writerow(list)
	file.close()
	os.rename(key,key+".csv")