#!/Python27/python
print("Content-type: text/html\n")
import urllib2
import re
import sys
import threading
import time
CLAN_NAME = "the+last+souls"
CLAN_API_URL = "http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName="
USER_API_URL = "http://services.runescape.com/m=hiscore/index_lite.ws?player="
failedurl = []
def connecturl(url):

	try:
		response = urllib2.urlopen(url)
		html = response.read()
		datastr = html.decode('Latin-1')
		response.close()
		return datastr
	except urllib2.HTTPError, err:
		if err.code == 404:
			# User is non member
			return None
		else:
			return 'failed'

def geturluserlist():
	datastr = connecturl(CLAN_API_URL + CLAN_NAME)
	un = re.compile('\n[^,]*')
	userlist = un.findall(datastr)
	finaluser = []
	# Creates url friendly names
	for user in userlist:
		user = user.replace('\n','')
		user = user.replace(u"\u00A0", '+')
		user = user.replace(' ', '+')
		finaluser.append(user)
	return finaluser

def getalluserdata(user, ud):
	global nonmem
	global clanmembers
	userdata = connecturl(USER_API_URL + user)
	if userdata == None:
		nonmem.write(user + '\n')
		return
	if userdata == 'failed':
		clanmembers.append(user)
		return
	ud.append([user,userdata])
	return

# Main code here
ur = re.compile('[^,]*')
rank = []
userdata = []
clanmembers = geturluserlist()


# pulls all clan data 
# for clan in clanmembers:
# 		if(threading.active_count() > 50):
# 			# Prevents massive badlinestatus (jagex blocking mass visits)
# 			time.sleep(3)
# 		thread = threading.Thread(None, getalluserdata, None, (clan,userdata,))
# 		thread.start()
# while(threading.active_count() > 1):
# 	time.sleep(5)

#sorts user data on rank
"""for user in userdata:
	rank.append([user[0], ur.search(user[1]).group(0)])
rank.sort(key=lambda mem: int(mem[1]))
rp = 0
f = open('clanrank.txt', 'w')
for r in rank:
	rp = rp + 1
	print(str(rp) + "   " + r[0] + '\n')
	"""