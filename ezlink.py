from genericpath import isfile
from pathlib import Path
import os
import magic
import sys

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

# loop through subdirectories
def loop_dir(src, dst, file_list):
	mime = magic.Magic(mime=True)   # required for magic library to identify file types

	for item in os.listdir(src):
		item_path = src+item
		# print(item_path)

		# if current item is a file
		if os.path.isfile(item_path):
			# print("Is File:\t"+item)

			filename = mime.from_file(item_path)

			# if file is a video
			if filename.find('video') != -1:
				# print("Is Video:\t"+item)
				file_list.append(os.path.abspath(item_path))
				try:
					os.symlink(item_path, dst+item)
				except(FileExistsError):
					continue

		# if current item is a directory
		# elif os.path.isdir(item_path):
		else:
			item_path = get_dir_path(item_path)
			# print("Is Dire:\t"+item_path)
			# print(item_path+"\n"+item_path)
			# print(os.path.abspath(item_path))
			loop_dir(item_path, dst, file_list)

def main():
	dst = "../Videos/All/"
	src = "../Videos"
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
	loop_dir(get_dir_path(src), get_dir_path(dst), file_list)
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
