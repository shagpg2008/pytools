#!/usr/bin/python

import zipfile, os

def zip_dirs(dir):
	__list = os.listdir(dir) 
	
	for file in __list:
		__path = os.path.join(dir,file)
		
		if file == '.':
			continue
		if os.path.isfile(__path):
			continue
		elif os.path.isdir(__path):
			cmd = 'python -m zipfile -c ' + file + '.zip '+ file + '/'
			print(cmd)
			os.popen(cmd)


zip_dirs(os.getcwd())
