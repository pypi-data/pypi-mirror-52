#coding=utf-8
import os
import json

def read_config(p='config.json'):
	'''
	return a dict formated config file
	if file open error, then return a empty dict
	'''
	try:
		return json.loads(read_file(p))
	except:
		return {}

def save_config(d,p='config.json'):
	'''
	save_conf, for dict type data
	'''
	save_file(p,json.dumps(d, sort_keys=True, indent=4),p +' updated')

def save_file(name,s,m='',t = 'w'):
	'''
	write to file
	do not use this for large files
	you can use this to print messages
	'''
	f = open(name,t)
	f.write(s)
	f.close()
	if not m=='':
		print(m)

def read_file(p,mode='r'):
	'''
	read file and return data
	do not use this for large files
	'''
	f = open(p)
	data = f.read()
	f.close()
	return data

def empty_folder(str_path_to_folder):
	'''
	remove all files in this folder
	print error message if failed
	'''
	for the_file in os.listdir(str_path_to_folder):
		file_path = os.path.join(str_path_to_folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)

def split_big_file_by_line_number(path,line_num = 60000):

	'''
	split big file, not working properlly
	'''
	f_r = open(path,'r')
	name,extension = path.split('.')
	count = 0
	sub_file_num = 0
	out_f = open(name+'_{0}.{1}'.format(sub_file_num,extension),'w')
	for line in f_r:
		out_f.write(line)
		count+=1
		if count==line_num:
			count = 0
			out_f.close()
			sub_file_num+=1
			out_f = open(name+'_{0}.{1}'.format(sub_file_num,extension),'w')
	out_f.close()
	if count==0:
		os.unlink(name+'_{0}.{1}'.format(sub_file_num,extension))

def filter_folder(path = '',filter_out_flag=False,key_words =[]):
	'''
	path: a string of the path. default is '',means use current folder.
	filter_out_flag: a boolean indicating whether is include or exclude key words
	key_words: a list of strings. default is empty, will return all files inside
	ignore folders inside
	list files with or without specifical key words
	if keyword list is empty, then returns all files in that folder
	'''
	if path=='':
		raw_file_list = os.listdir()
	else:
		raw_file_list = os.listdir(path)
	temp = []
	for item in raw_file_list:
		if os.path.isfile(os.path.join(path,item)):
			temp.append(os.path.join(path,item))
	raw_file_list = temp
	have_keywords = []
	no_keywords = []
	if key_words == []:
		return raw_file_list
	for f in raw_file_list:
		for keyword in key_words:
			if f.find(keyword)>=0:
				have_keywords.append(f)
			else:
				no_keywords.append(f)
	have_keywords = list((set(have_keywords)))
	no_keywords = list((set(no_keywords)))
	if filter_out_flag:
		return no_keywords
	else:
		return have_keywords

def filter_folder_recursively(path = '',filter_out_flag=False,key_words =[]):
	'''
	ignore folders inside
	list files with or without specifical key words
	if keyword list is empty, then returns all files in that folder
	'''

	if path=='':
		raw_file_list = os.listdir()
	else:
		raw_file_list = os.listdir(path)
	raw_file_list = map(lambda x: os.path.join(path,x),raw_file_list)

	temp = []
	folders = []
	for item in raw_file_list:
		if os.path.isfile(item):
			temp.append(item)
		elif os.path.isdir(item):
			folders.append(item)
	sub_result = []

	for folder in folders:
		sub_result += filter_folder_recursively(os.path.join(path,folder),filter_out_flag,key_words)
	raw_file_list = temp
	have_keywords = []
	no_keywords = []

	if key_words == []:
		return raw_file_list + sub_result
	for f in raw_file_list:
		for keyword in key_words:
			if f.find(keyword) >= 0:
				have_keywords.append(f )
			else:
				no_keywords.append(f )
	
	if filter_out_flag:
		return no_keywords + sub_result
	else:
		return have_keywords + sub_result
			
def remove_empty_folder(path='',escape = ['System Volume Information','$RECYCLE.BIN']):
	'''
	remove all empty folders with in the given path recursively
	'''
	if path=='':
		raw_list = os.listdir()
	else:
		raw_list = os.listdir(path)
	folders = []
	for item in raw_list:
		if os.path.isdir(os.path.join(path,item)) and (item not in escape):
			folders.append(item)
	for folder in folders:
		this_path = os.path.join(path,folder)
		if len(os.listdir(this_path))>0:
			remove_empty_folder(path = this_path)
		try:
			os.rmdir(this_path)
			# print('{0} deleted!'.format(this_path))
		except:
			pass

def get_new_name(base_name,num,ext):
	'''add num until get a file name that do not exist'''

	name = '{0}_{1}.{2}'.format(base_name,num,ext)
	while os.path.isfile(name):
		num += 1
		name = '{0}_{1}.{2}'.format(base_name,num,ext)
	return name

def split_big_file(path):
	if os.path.isfile(path):
		split_big_file_by_line(path)
	elif os.path.isdir(path):
		files = os.listdir(path)
		for f in files:
			split_big_file_by_line(path+f)

def split_big_file_by_line(path,size = 1000*10):
	'''
	split a big file based on line

	'''
	if os.path.isfile(path):
		f = open(path,'r')
		tail = path.split('.')[-1]
		base_name = path[:-len(tail)-1]

		temp = []
		sub_num = 0
		for line in f:
			if len(temp)<size:
				temp.append(line)
			else:
				f_o = open(get_new_name(base_name,sub_num,tail),'w')
				f_o.writelines(temp)
				f_o.close()
				temp = []
		f_o = open(get_new_name(base_name,sub_num,tail),'w')
		f_o.writelines(temp)
		f_o.close()
		f.close()
		os.unlink(path)


if __name__ == "__main__":
	pass
