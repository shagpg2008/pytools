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

import os,sys,re,time

_line_comment1 = re.compile(r'//.*')
_line_comment2 = re.compile(r'/\*.*\*/')
_lines_comment_start = re.compile(r'/\*.*')
_lines_comment_stop  = re.compile(r'.*\*/')
_matched_file = re.compile('\.(h|hpp)$')
_matched_xml_file = re.compile('\.xml$')
_path_root = os.getcwd()

def getStructRe(key):
	return re.compile(r'(struct|class|union)[\t ]+([\w_]+)[\t ]*\{[\t ;:\[\]\(\)\w_]*\b%s\b[\t ;\[\]\(\)\w:]+\}[\t \w_\(\)]*;'%key)
def getTypedefRe(key):
	return re.compile(r'(typedef)[\t ]+\b%s\b[\t ]+([\w_]+)[\t ]*;'%key)

def stripComment(__lines):
	global _line_comment1;
	global _line_comment2;
	global _lines_comment_start;
	global _lines_comment_stop;
	_is_lines_comment_mode = 0
	_text = ''
	
	for line in __lines:
		if _is_lines_comment_mode:
			__modified_line = _lines_comment_stop.sub(str(''), line)
			if(line != __modified_line):
				_is_lines_comment_mode = 0
				line = __modified_line
			else:
				continue
		
		line = _line_comment1.sub('', line)
		
		while True:
			__modified_line = _line_comment2.sub(str(''), line)
			if __modified_line == line:
				break
			line = __modified_line

		__modified_line = _lines_comment_start.sub(str(''), line)
		if(line != __modified_line):
			_is_lines_comment_mode = 1

		_text += __modified_line.strip()
	return _text

def searchFile(filename, search_tag):
	__file = open(filename, 'r',encoding='utf-8')
	try:
		__lines = __file.readlines()
	except Exception as err:
		print(err)
		print('file:%s'%filename)
		__file.close()
		return ''
	__file.close()
	__name = str('')
	
	__text = stripComment(__lines)
	
	_m = search_tag.search(__text)
	
	if _m :
		__name = _m.group(2)
	return __name

def searchFiles(_path_root, search_tag, parent, op):
	global _matched_file
	__list = os.listdir(_path_root) 
	
	for i in range(0,len(__list)):
		__path = os.path.join(_path_root,__list[i])
		
		if __list[i][0] == '.':
			continue
		if os.path.isfile(__path):
			if not _matched_file.findall(__list[i]) :
				continue
			ref_type_name = searchFile(__path, search_tag)
			if ref_type_name :
				op(parent, ref_type_name)
		elif os.path.isdir(__path):
			searchFiles(__path, search_tag, parent, op)

def searchFilesStruct(search_tag, parent):
	def structOp(p, name):
		if len(p) > 1:
			tmp = [name]
			p[1].append(tmp)
		else:
			tmp = [[name]]
			p.append(tmp)
	global _path_root
	searchFiles(_path_root, search_tag, parent, structOp)

def searchFilesTypedef(search_tag, parent):
	def typedefOp(p, name):
		tmp = [name]
		if len(p) <= 1:
			p.append(tmp)
		else:
			p[1].append(tmp)
	
	global _path_root
	searchFiles(_path_root, search_tag, parent, typedefOp)

def searchKeys(parent):
	__key = parent[0]
	print('Search %s ...'%__key)
	searchFilesStruct(getStructRe(__key), parent);

	if len(parent) <= 1:
		return
	
	for __key in parent[1]:
		searchFilesTypedef(getTypedefRe(__key[0]), parent);
		searchKeys(__key)

def searchREL(key):
	type_list = [key]
	output = ''
	
	searchFilesTypedef(getTypedefRe(key), type_list);
	searchKeys(type_list)
	print('')
	output += printLeaves(type_list)
	output += printEnvokeRelation(type_list)
	print(output)
	__file = open(key+'.txt', 'w',encoding='utf-8')
	__file.write(output)
	__file.close()
	
def getLeaf(leaves, typeItem):
	if len(typeItem) <= 1:
		leaves.add(typeItem[0])
	else:
		for item in typeItem[1]:
			getLeaf(leaves, item)

def printLeaves(typeList):
	leaves = set()
	getLeaf(leaves, typeList)
	retStr = '%s invoked by:\n' % typeList[0]
	for leaf in leaves:
		retStr += '\t%s\n' % leaf
	retStr += '\n'
	return retStr

def getEnvokeRel(relList, relStr, parent):
	base = relStr.copy()
	base.insert(0, parent[0])
	is_need_copy = 0
	
	if len(parent) > 1:
		for item in parent[1]:
			tmp = base
			if is_need_copy:
				tmp = base.copy()
			is_need_copy = 1
			getEnvokeRel(relList, tmp, item)
	else:
		relList.append(base)

def printEnvokeRelation(typeList):
	relList = []
	getEnvokeRel(relList, [], typeList)
	retStr = 'The type relationships:\n'
	index = 1
	
	for rel in relList:
		retStr += '%d. %s\n' %(index, rel[0])
		i = 1
		indentTags = '\t'
		
		while i < len(rel):
			retStr += indentTags + rel[i] + '\n'
			indentTags += '\t'
			i += 1
		index += 1
	return retStr

if len(sys.argv) != 2:
	print('./' + os.path.basename(__file__) + ' <key-type-name>')
else:
	searchREL(sys.argv[1])
