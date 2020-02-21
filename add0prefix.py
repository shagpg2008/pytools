#!/usr/bin/python
################################################################
#
# Script description: the tool is for padding 0 for those without
#	   0 in the filename. for example: 1.txt, 10.txt. then change
#	   1.txt to 01.txt
# Author: Liao Shuangping
# Date: 2020.02.21
#
################################################################

import os,sys,re,time

fileList = {}
def split_num(_str):
	num = ""
	index = 0;
	while _str[index] >= '0' and _str[index] <= '9':
		num += _str[index]
		index += 1
	return (int(num),_str[index:])

def find_max_num(_path_root):
	global fileList
	max_num = 0
	
	__list = os.listdir(_path_root) 
	
	for i in range(0,len(__list)):
		__path = os.path.join(_path_root,__list[i])
		
		if os.path.isfile(__path) and __list[i][0] >= '0' and __list[i][0] <= '9':
			file_name_num = split_num(__list[i])
			fileList[__list[i]] = file_name_num
			if(max_num < file_name_num[0]):
				max_num = file_name_num[0]
	return max_num

def get_num_base(_num):
	if _num < 10:
		return 1
	elif _num < 100:
		return 2
	elif _num < 1000:
		return 3
	elif _num < 10000:
		return 4
	else:
		print("Too big file index max=%d", _num)
		return 5

def add_0padding_file(_path_root, num_0s):
	global fileList	
	
	if num_0s < 2:
		return
	
	prefix0 = "%0" + str(num_0s) + "d"
	for (file_name, num_name) in fileList.items():
		new_file_name = prefix0 % num_name[0] + num_name[1]
		if new_file_name != file_name:
			__path = os.path.join(_path_root,file_name)
			__dst  = os.path.join(_path_root,new_file_name)
			print("Rename \"%s:\"(%s --> %s)" % ( _path_root, file_name, new_file_name))
			os.rename(__path, __dst);
			
def add_0_dir(_path_root):
	global fileList
	fileList = {}
	max_num = find_max_num(_path_root)
	num_0s = get_num_base(max_num)
	add_0padding_file(_path_root, num_0s)
	
def add_0_dirs(_path_root):
	add_0_dir(_path_root)
	__list = os.listdir(_path_root) 
	
	for i in range(0,len(__list)):
		__path = os.path.join(_path_root,__list[i])
		if os.path.isdir(__path):
			add_0_dir(__path)

add_0_dirs(os.getcwd())

