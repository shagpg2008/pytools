#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys,os
import time

time1=time.time()
print ("Start to commit code...")
count=0
def re_exe(cmd, inc = 60): 
	while True:
		global count
		r = os.popen("svn ci -F log.txt")
		info = r.readlines()
		count += 1
		print ("Committed " + str(count) + " times" )
		for line in info:
			line = line.strip('\r\n')
			print (line)
			if line.find("Committed revision")>=0:
				print ("Commit code successfully!!!")
				return
			if line.find("out of date")>=0:
				os.popen("svn up")
		time.sleep(inc)
	
re_exe("echo %time%")

time2 = time.time()

print (u'Total time:', str(time2 - time1), 's')

