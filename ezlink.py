import os
import sys
from pathlib import Path

import magic
from genericpath import isfile

mime = magic.Magic(mime=True)   # required for magic library to identify file types

# convert a path to unix path
def unix_path(path):
	if isinstance(path, str):
		return path.replace(" ", "\\ ")

# adds the '/' at the end of a directory
def get_dir_path(item):
	if os.path.isdir(item):
		return item+'/'
	return item

# remove current linked files
def rem_all_links(path):
	if len(os.listdir(path)) > 0:
		os.system('rm '+unix_path(path)+'*')

def loop_dir(src, dst, counter=-1):
	file_list = []
	dir_list = []
	all_list = os.listdir(src)

	while True:
		new_dir = True

		for item in all_list:
			item_path = src+item

			# if current item is a file
			if os.path.isfile(item_path):
				file_type = mime.from_file(item_path)

				# if file is of required type
				if file_type.find('audio') != -1:
					# append counter to filename if option was enabled
					if counter >= 0:
						if new_dir:
							counter += 1
							new_dir = False
						file_list.append(dst+str(counter)+" "+item)
					else:
						file_list.append(dst+item)

			# if current item is a sub directory
			else:
				dir_list.append(get_dir_path(item_path))
	
		if len(dir_list) == 0:
			break
		else:
			all_list = dir_list[:]
			dir_list.clear()
	
	return file_list



# loop through subdirectories
# def loop_dir(src, dst, file_list, counter = -1, new_sub_dir = False):
	# mime = magic.Magic(mime=True)   # required for magic library to identify file types

	for item in os.listdir(src):
		item_path = src+item
		# print(item_path)

		# if current item is a file
		if os.path.isfile(item_path):
			# print("Is File:\t"+item)
			# print(magic.from_file(item_path))

			file_type = mime.from_file(item_path)
			# print (file_type)

			# if file is of required type
			if file_type.find('audio') != -1:

				# mark new dir if file type matches (for counter)
				if new_sub_dir is False:
					new_sub_dir = True

				# print("Is Video:\t"+item)
				# file_list.append(os.path.abspath(item_path))

				# append counter to filename if option was enabled
				if counter >= 0:
					file_list.append(dst+str(counter)+" "+item)
				else:
					file_list.append(dst+item)
				# try:
				# 	os.symlink(item_path, dst+item)
				# except(FileExistsError):
				# 	continue

		# if current item is a directory
		else:
			item_path = get_dir_path(item_path)
			# print("Is Dire:\t"+item_path)
			# print(item_path+"\n"+item_path)
			# print(os.path.abspath(item_path))
			# print(new_sub_dir)
			if new_sub_dir and counter >= 0:
				counter += 1
				# print(counter)

			loop_dir(item_path, dst, file_list, counter, new_sub_dir)

def main():
	# dst = "../../All/"
	# src = "../../"
	# dst = "../"
	# src = "../"
	dst = "/home/rez/ramdisk/"
	src = "/home/rez/ramdisk/"
	file_list = []

	# test listdir
	file_paths = []

	# print(os.path.abspath(src))
	# folder, subs, files = os.walk(src)
	# print(os.walk(src))

	# for folder, subs, files in os.walk(src):
	#     for filename in files:
	#         file_paths.append(os.path.abspath(os.path.join(folder, filename)))
	# for x in file_paths:
	#     print(x)

	# rem_all_links(dst)
	src = os.path.abspath(src)
	dst = os.path.abspath(dst)
	# loop_dir(get_dir_path(src), get_dir_path(dst), file_list, counter=0)
	file_list = loop_dir(get_dir_path(src), get_dir_path(dst))
	for file in file_list:
		print(file)

	# if len(sys.argv) != 3:
	#     print("Expected 2 arguments (src, dst). Received: "+str(sys.argv[1:]))
	# else:
	#     for path in sys.argv[1:]:
	#         print(unix_path(path))

	# print(os.path.abspath("GasNotify/"))


if __name__ == "__main__":
	main()
