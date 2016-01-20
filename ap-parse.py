#!usr/bin/python
import re

logfile = open("result", "r").readlines()
#KEYWORDS = ['ESSID:"', 'Quality=']
aps = []
counter = 0
for line in logfile:
	tmp=re.findall(r'"(.*?)"', line)
	if tmp is None:
		print "blocked"
	else:
		aps.append(tmp)

aps = filter(None, aps)

print aps
