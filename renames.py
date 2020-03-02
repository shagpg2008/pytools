#!/usr/bin/python

import os,sys,re,time

def mvfiles(dir, matched_pattern, replaced_pattern):
	__list = os.listdir(dir) 
	_matched_file = re.compile(matched_pattern);
	
	for file in __list:
		__path = os.path.join(dir,file)
		
		if file == '.':
			continue
		else:
			new_name = _matched_file.sub(replaced_pattern, file, 1)
			
			if new_name != file:
				__dst = os.path.join(dir, new_name)
				os.rename(__path, __dst);
				__path = __dst
			
			if os.path.isdir(__path):
				mvfiles(__path, matched_pattern, replaced_pattern)

if len(sys.argv) != 3:
	print( './' + os.path.basename(__file__) + '<MATCHED_PATTERN> <REPLACED_PATTERN>')
else:
	mvfiles(os.getcwd(), sys.argv[1], sys.argv[2])
	
