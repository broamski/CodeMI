import fileinput
import time
import json
import urllib2
import sys
import os

def fact_finder(obj):
	key =  obj[0].strip()
	value = obj[1].strip()
	global facilityName, county, primaryRoute, localRoute, exitNumber, quad, capacity, count, surfaceType, entranceSign, light
	global county
	if key == "Facility Name":
		facilityName = value
	elif key == "County":
		county = value
	elif key == "Primary Route":
		primaryRoute = value
	elif key == "Local Route":
		localRoute = value
	elif key == "Exit Number":
		exitNumber = value
	elif key == "Quad":
		quad = value
	elif key == "Capacity":
		capacity = value
	elif key == "Count":
		count = value
	elif key == "Surface Type":
		surfaceType = value
	elif key == "Entrance Sign":
		entranceSign = value
	elif key == "Light":
		light = value


fo = open("/home/brian/list.txt", "r")
fw = open("/home/brian/output.csv", "ab")

for key in fo:
	key = key.strip(' \t\n\r')
	data = urllib2.urlopen('http://mdotcf.state.mi.us/public/carpoolpark/report.cfm?key=' + key)
	request_data = data.read()
	#print request_data

	from bs4 import BeautifulSoup
	soup = BeautifulSoup(request_data)

	tables = soup.find("table")

	for row in tables.findAll("tr"):
	    cells = row.findAll("td")
	    for cell in cells:
	    	cell_lines = cell.get_text().split('\n')
	    	for cell_line in cell_lines:
	    		ugk = cell_line.split(":")
	    		if len(ugk) == 2:
	    			fact_finder(ugk)
	output_line = key + "," + facilityName + "," + county + "," + primaryRoute + "," + localRoute + "," + exitNumber + "," + quad + "," + capacity + "," + count + "," + surfaceType + "," + entranceSign + "," + light
	print("Writing " + output_line + "...")
	fw.write(output_line + "\r\n")
	#print(key + "," + facilityName + "," + county + "," + primaryRoute + "," + localRoute + "," + exitNumber + "," + quad + "," + capacity + "," + count + "," + surfaceType + "," + entranceSign + "," + light)

	# Don't want to slam SOM's boxes...
	time.sleep(1)
fw.close()
fo.close()
