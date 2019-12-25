#!/usr/bin/python
################################################################
#
# Script description: the tool is for search the type used in
#	   other structure, class, union and typedef types. They're
#	   based on python regular expression and C/C++ head files.
# Author: Liao Shuangping
# Date: 2019.12.17
#
################################################################

import os,sys,shutil


def delSVNFolders(_path_root):
	__list = os.listdir(_path_root) 
	
	for i in range(0,len(__list)):
		__path = os.path.join(_path_root,__list[i])
		
		if os.path.isdir(__path):
			if __list[i] == '.svn':
				print (__list[i])
				shutil.rmtree(__path)
			else:
				delSVNFolders(__path)

delSVNFolders(os.path.dirname(os.path.realpath(__file__)))