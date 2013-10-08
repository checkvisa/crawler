#!/usr/bin/python

import urllib2
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pymongo import MongoClient

db = MongoClient('mongodb://admin:admin@192.241.221.190/checkoo')
database = db.checkoo
Data_collection = database.Checkee
Data_collection.drop()

majorDict = {}
with open('./mdict', 'r') as major:
	for line in major:
		key, value = line.strip().split(' ==> ')
		majorDict[key] = value

utc = datetime.utcnow()
if int(str(utc).split()[1].split(":")[0])>=16:
	dispdate = str(utc - timedelta(days=9999)).split()[0]
else:
	dispdate = str(utc - timedelta(days=10000)).split()[0]
url = "http://www.checkee.info/main.php?dispdate="+dispdate
print url

page = urllib2.urlopen(url)
soup = BeautifulSoup(page)
checkoo = []
for tr in soup.find_all('tr'):
	check = []
	for td in tr.find_all('td'):
		check.append(td.string)
	# skip unwanted tables
	if len(check)!=11: continue
	if check[0]=='BeiJing': continue
	if check[6]=='Status': continue
	# skip waiting days larger than 1000 days
	if int(check[9])>1000: continue
	# skip 2013 data
	# if check[7][:4]=='2013':continue
	try:
		major = majorDict[check[5].lower()]
		# print major
	except:
		major = "N/A"
	checko = {
	    "ID": check[1],
	    "VisaType": check[2],
	    "VisaEntry": check[3],
	    "City": check[4],
	    "Major": major,
	    "Status": check[6],
	    "CheckDate": check[7],
	    "CompleteDate": check[8],
	    "WaitingDays": int(check[9])
  	}
  	checkoo.append(checko)
Data_collection.insert(checkoo)

