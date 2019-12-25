#!/usr/bin/python

import os,sys,re,time

def mvfiles(dir, matched_pattern, replaced_pattern):
	__list = os.listdir(dir) 
	_matched_file = re.compile(matched_pattern);
	
	for file in __list:
		__path = os.path.join(dir,file)
		
		if file == '.':
			continue
		if os.path.isfile(__path):
			new_name = _matched_file.sub(replaced_pattern, file, 1)
			__dst = os.path.join(dir, new_name)
			os.rename(__path, __dst);

if len(sys.argv) != 4:
	print './' + os.path.basename(__file__) + '<DIR> <MATCHED_PATTERN> <REPLACED_PATTERN>'
else:
	mvfiles(sys.argv[1], sys.argv[2], sys.argv[3])
	
