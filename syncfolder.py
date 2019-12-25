#!/usr/bin/python

import os,sys,re,time,datetime,shutil

folder1Dict = {}
folder2Dict = {}

def get_file_list(root_dir):   
	__L={}
	#print "root_dir=",root_dir
	for root, dirs, files in os.walk(root_dir):  
		for file in files:
			file_name = os.path.join(root, file)
			__L[file_name] = (os.path.getsize(file_name), os.path.getmtime(file_name)) #getsize,getmtime
		for dir in dirs:
			get_file_list(os.path.join(root, dir));
	#print __L
	return __L

def unique_file_list(indexLeft1, dir2):
	global folder1Dict, folder2Dict
	#print 'before unique: dict1:', folder1Dict
	#print 'before unique: dict2:', folder2Dict
	__file_list = folder1Dict.keys()
	#print 'before unique: file_list:', __file_list
	for file in __file_list:
		file2 = dir2 + file[indexLeft1:]
		if folder2Dict.has_key(file2):
			if folder1Dict[file][0] == folder2Dict[file2][0]:
				folder1Dict.pop(file)
				folder2Dict.pop(file2)
			elif folder1Dict[file][1] < folder2Dict[file2][1]:
				folder1Dict.pop(file)
			else:
				folder2Dict.pop(file2)
	print '\n\nafter unique: dict1:', folder1Dict
	print 'after unique: dict2:', folder2Dict
	
def copy_file_list(dict, leftIndex, dst_dir):
	for file in dict:
		__dst_file = dst_dir + file[leftIndex:]
		#print 'dst_file = ', __dst_file
		__dst_file_dir = os.path.dirname(__dst_file)
		#print '__dst_file_dir =',__dst_file_dir
		if not os.path.exists(__dst_file_dir):
			os.makedirs(__dst_file_dir)
		
		print 'copyfile: %s -> %s' % (file, __dst_file)
		shutil.copyfile(file, __dst_file)

if len(sys.argv) != 3:
	print './' + os.path.basename(__file__) + ' <folder1> <folder2>'
else:
	folder1Dict = get_file_list(sys.argv[1])
	folder2Dict = get_file_list(sys.argv[2])
	unique_file_list(len(sys.argv[1]), sys.argv[2])
	copy_file_list(folder1Dict, len(sys.argv[1]), sys.argv[2]);
	copy_file_list(folder2Dict, len(sys.argv[2]), sys.argv[1]);
