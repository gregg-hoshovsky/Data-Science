import os, os.path
import time

import sys 
from collections import namedtuple

	
# name is the NAME from the  caller id
# number is the NMBR from the caller id
# status is a way to communicate to this server
# statusOptions can subset the status. right now the keyboard status may need
#	lower, upper, digits, puncuation as subcomponents
QueueData = namedtuple("QueueData", "name number status statusOption")

filePath="./images"
filePathCallers=filePath+"/callers"
filePathScreenSavers=filePath+"/screensavers"


def totalScreenSaverCount():
	total = 0
	for name in os.listdir(filePathScreenSavers):
		#print("tfile {0}".format(name))
		if os.path.isfile(filePathScreenSavers+"/"+name):
			total=total+1
	#print("total SS {0}".format(total))
	return total
	
def monitorQueue():
	print ("name: ")
	nme = sys.stdin.readline()
	print ("number: ")
	nmbr= sys.stdin.readline()
	print ("status: ")
	stat= sys.stdin.readline()
	m = QueueData(name = nme.rstrip(), number = nmbr.rstrip(), status = stat.rstrip(), statusOption="")
	return m	
	
def displayScreenSaver(screenSaverCount):
	print (" displayScreenSaver {0}".format(screenSaverCount))
	list_dir = []
	list_dir = os.listdir(filePathScreenSavers)
	count = 0
	for file in list_dir:
		if count== screenSaverCount:
			img="{0}/{1}".format(filePathScreenSavers,file)
			display(img)
			return
		count += 1
		
def displayReset():
	print (" displayReset ")
def displaykeyboard():
	print (" displaykeyboard ")
def displayCallerIdNoImage(q):
	print (" displayCallerId {0} {1}".format(q.number,q.name))
def display(img):
	print (" display {0} ".format(img))
def imageDisplay(n):
	imgList=["png","jpg","gif"];
	print (" imageDisplay {0} ".format(n))
	for i in imgList:
		img="{0}/{1}.{2}".format(filePathCallers,n,i)
		try:
			if os.path.isfile(img) :
				display(img)
				return True
		except: 
			pass	
	return False
	
def displayCallerId(cc):
		if  imageDisplay(cc.number):
			return
		displayCallerIdNoImage(cc)
		
		
def main():
	timeout=5 # seconds
	timer =0
	displayStatus="screensaver"
	screenSaverCount=0
	current_call=QueueData(name = "No One", number = "UnKnown", status = "screensaver", statusOption="")

	timer = time.clock()

 

	while True:
		# monitor the queue. if we are not being asked to display anything
		# then keep rotation thru the screen savers.
		time.sleep(.5)
		queData=monitorQueue();
		elapsed = (time.clock() - timer)
		print("elased time {0}".format(elapsed));
		if queData.status == "":
			if elapsed > timeout:
				timer = time.clock()
				displayScreenSaver(screenSaverCount)
				screenSaverCount=screenSaverCount+1
				if screenSaverCount >= totalScreenSaverCount():
					screenSaverCount=0;
			continue
			
		print (queData)
		# recieved a call so we want stop the screen saver for alteast 5 minutes more to work
		# we need to process the request and manage the display. we may not
		# be the only manager. If this is the case who ever is manager the screen 
		# say the keybaord handler. They better send us a noop so we don't let the
		# screen saver kick back in.
		timer=time.clock()
		if queData.status == "noop":
			# do nothing, someone is managing the screen
			continue
		elif queData.status == "caller_id":
			displayStatus=queData.status
			current_call=queData
			displayCallerId(current_call);
		elif queData.status == "reset":
			displayReset()
		elif queData.status == "blacklist":
			displayBlackList(queData)
			displayStatus=queData.status
		elif  queData.status == "keyboard":
			displaykeyboard()
			displayStatus=queData.status	
			
		# if we are asked to attention usually by a touch screen
		# check to see what we were doing before the screen saver was running
		elif queData.status == "attention":
			if displayStatus== "caller_id":
				displayCallerId(current_call)
			elif displayStatus== "keyboard":
				displaykeyboard()
			elif displayStatus == "reset":
				displayReset()
			else:
				displayScreenSaver(screenSaverCount)
				

	

	
if __name__ == "__main__":
    main()