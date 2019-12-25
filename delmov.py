import os

curr_path = os.getcwd()
print curr_path

pathDir  = os.listdir(curr_path)
print pathDir

for file in pathDir:
	temp = file.split('.')
	if temp[-1] != "MOV":
		continue
	
	jpgFile = os.path.join('%s\\%s.JPG' % (curr_path, temp[0]))
	if os.path.exists(jpgFile):
		print jpgFile, "  exist...."
		movFile = os.path.join('%s\\%s' % (curr_path, file))
		print movFile, "remove ...."
		os.remove(movFile)