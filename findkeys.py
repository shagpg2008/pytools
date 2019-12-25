#!/usr/bin/python

import os,sys,re,time

def search_file_with_key(filename, key):
	__file = open(filename, 'rb')
	__res = '\t' + filename + ':\n'
	__isblank = 1
	__line_number = 1
	for x in __file.readlines():
		__matchstr = key.findall(x)
		if __matchstr:
			__res += '\t\t' + str(__line_number) +':' + x
			__isblank = 0
		__line_number += 1
	__file.close()
	if __isblank == 1:
		__res = ''
	return __res;

def search_one_key(res_file, dir_name, key):
	__list = os.listdir(dir_name) 
	_matched_file = re.compile('\.(rtm|xml)');
	
	for i in range(0,len(__list)):
		__path = os.path.join(dir_name,__list[i])
		
		if __list[i][0] == '.':
			continue
		if os.path.isfile(__path):
			if not _matched_file.findall(__list[i]) :
				continue
			print __path
			__res = search_file_with_key(__path, key)
			if __res:
				res_file.write(__res);
		elif os.path.isdir(__path):
			search_one_key(res_file, __path, key)

def search_keys_in_file(key_file):
	__key_file = open(key_file, 'rb')
	__res_file = open(key_file+'.out', 'ab');
	__res_file.write('\n\n--------------[['+time.asctime( time.localtime(time.time()) ) + ']] --------------\n')
	for _key in __key_file.readlines():
		_key = _key.strip();
		_re  = re.compile(_key)
		__res_file.write(_key+':\n');
		search_one_key(__res_file, os.path.dirname(os.path.realpath(__file__)), _re)
	__key_file.close()
	__res_file.close()

if len(sys.argv) != 2:
	print './' + os.path.basename(__file__) + ' <key-file-name>'
else:
	search_keys_in_file(sys.argv[1])
