#!/usr/bin/python
#############################################################
#
# Script description: the tool is for search and replace huge
#       complex key-values with boundary. The key and values
#       are based on python regular expression.
# Author: Liao Shuangping
# Date: 2019.04.17
#
#############################################################

import os,sys,re,time

rules = (
	#Match Mode: ('start_expr', 'end_expr', (('key1', 'value1'), ('key2', 'value2'), ............. )), .............
	('sendXML<PS_HoUeAddReq>[\r\n\t ]*\(', '\)', (('[\t ]*container_discriminator[\t \r\n,=>\w\$]*', ''), ('container_', ''))),
	('name="PS_HoUeAddReq"', '<\/message>', (('container_', ''), ('',''))),
	('sendXML<PS_RbAddReq>[\r\n\t ]*\(', '\)', (('[\t ]*container_discriminator[\t \r\n,=>\w\$]*', ''), ('container_', ''), ('hasContainer','hasWmpUserContainer'))),
	('name="PS_RbAddReq"', '<\/message>', (('container_', ''), ('hasContainer','hasWmpUserContainer')))
	)

file_lines = ['','']
	
def replaceLine(line, subList):
	for _pattern in subList:
		_replaced = re.sub(_pattern[0], _pattern[1], line,1)
		line = _replaced;
	return line;
	
def replaceLines(rule):
	global file_lines
	_re_start_tag = re.compile(rule[0]);
	_re_stop_tag = re.compile(rule[1]);
	_is_need_replace = 0
	_is_content_changed = 0
	
	for index in range(len(file_lines)):
		if not _is_need_replace:
			remove_comment = re.sub('#.*', '', file_lines[index])
			if _re_start_tag.search(remove_comment):
				_is_need_replace = 1
		if _is_need_replace:
			_line = replaceLine(file_lines[index], rule[2])
			if not _is_content_changed:
				if _line != file_lines[index]:
					_is_content_changed = 1
			file_lines[index] = _line
			remove_comment = re.sub('#.*', '', _line)
			if _re_stop_tag.search(remove_comment):
				_is_need_replace = 0
	return _is_content_changed		

def replaceFile(filename):
	_is_need_rewrite = 0
	print filename
	read_file_lines(filename)
	for rule in rules:
		_is_need_rewrite_temp = replaceLines(rule)
		if not _is_need_rewrite:
			_is_need_rewrite = _is_need_rewrite_temp
	if _is_need_rewrite:
		write_file_lines(filename)

def replaceFiles(dir_name):
	__list = os.listdir(dir_name) 
	_matched_file = re.compile('\.(rtm|xml)');
	
	for i in range(0,len(__list)):
		__path = os.path.join(dir_name,__list[i])
		
		if __list[i][0] == '.':
			continue
		if os.path.isfile(__path):
			if not _matched_file.findall(__list[i]) :
				continue
			replaceFile(__path)
		elif os.path.isdir(__path):
			replaceFiles(__path)

def read_file_lines(filename):
	global file_lines
	__file = open(filename, 'rb')
	file_lines = __file.readlines()
	__file.close()

def write_file_lines(filename):
	global file_lines
	__file = open(filename, 'wb')
	__file.writelines(file_lines)
	__file.close()
	
def test():
	global file_lines
	res = replaceLine('     	container_xxx=>12', rules[0][2])
	print res
	if res == '     	xxx=>12':
		print 'passed'
	else:
		print 'failed'

	res = replaceLine('     	container_discriminator=>12  \n', rules[0][2])
	print res
	if res == '':
		print 'passed'
	else:
		print 'failed'	
	#read_file_lines('Caselist.txt');
	#print file_lines
	
	#file_lines = ['  \tsendXML<PS_HoUeAddReq>\t ( \t', 
	#              '   container_discriminator    =>0,\n',
	#			'        container_wmpUserContainer_cqiParamsWmp_cqiAperPollT  =>$cqiAperPollT,\n',
	#			'        container_wmpUserContainer_cqiParamsWmp_cqiAperEnable =>$cqiAperEnable\t )\n']
	#_is_content_changed = replaceLines(rules[0])
	#if _is_content_changed:
	#	print file_lines
	#replaceFile('PsCommon/AddTtiBundlingUE.rtm')
	file_lines = ['xxxx\n', 'sendXML<PS_RbAddReq>(\n',
			'                        dstAddr               => $dlCoreCellSicad,\n',
			'                        cellId                => $lnCelId,\n',
			'                        crnti                 => $crnti,\n',
			'                        ueIndex               => $UeIndex,\n',
			'                        hasUeSetupParams       =>1,\n',
			'                        ueSetupParams_srEnable =>1,\n',
			'                        ueSetupParams_pucchResourceIndex =>0,\n',
			'                        ueSetupParams_srPeriod =>1, #10ms    (0-4) (5ms,10ms,20ms,40ms,80ms)\n',
			'                        ueSetupParams_srOffset =>7, #sfn = 7\n',
			'\n',
			'                        hasContainer=>1,\n',
			'                        container_wmpUserContainer_harqMaxTrDl=>3,\n',
			'                        container_wmpUserContainer_hasMaxNumOfLayers      => $hasMaxNumOfLayers,\n',
			'                        container_wmpUserContainer_maxLayersDeliveredToUe => $maxLayersDeliveredToUe,\n',
			'                        container_wmpUserContainer_maxNumOfLayers         => $maxNumOfLayers,\n',
			'                        hasUeParams                                       => 0,\n',
			'\n',
			'                        numRbs => 1,\n',
			'                        rbInfoList_drbId                          [0] => 5,\n',
			'                        rbInfoList_drbType                        [0] => 1,##NON GBR\n',
			'                        rbInfoList_logicalChannelId               [0] => 4,\n',
			'                        rbInfoList_logicalChannelGrId             [0] => 2,\n',
			'                        rbInfoList_wmpRbInfo_schedulWeight        [0] => 10,\n',
			'                        rbInfoList_wmpRbInfo_qci                  [0] => 6,##NON GBR\n',
			'                        rbInfoList_wmpRbInfo_hasNbrUl             [0] => 1,\n',
			'                        rbInfoList_wmpRbInfo_nbrUl                [0] => 100\n',
			'\n',
			'                        );\n']
	_changed = replaceLines(rules[2])
	print 'changed:', _changed
	print file_lines
#test()
#if len(sys.argv) != 2:
#	print './' + os.path.basename(__file__) + ' <key-file-name>'
#else:
#	search_keys_in_file(sys.argv[1])
#     	container_xxx=>12

#_matched_file = re.compile('\.(rtm|xml)');
#if  _matched_file.findall('TC_LTE3659_2_11_20M_CFG27_D15U3_TM4_4Layer_64QAM.rtm') :
	#print 'matched'

replaceFiles(os.path.dirname(os.path.realpath(__file__)))
