import os
import magic

mime = magic.Magic(mime=True)   # required for magic library to identify file types

# convert a path to unix path
def unix_path(path):
	if isinstance(path, str):
		return path.replace(" ", "\\ ")

# adds the '/' at the end of a directory
def get_dir_path(item):
	if os.path.isdir(item):
		if item[-1] != '/':
			return item+'/'
	return item

# remove current linked files
def rem_all_links(path):
	if len(os.listdir(path)) > 0:
		os.system('rm '+unix_path(path)+'*')

def find(src, dst, counter=False):
	file_list = []
	dir_list = []

	if counter == True:
		counter = 0
	else:
		print("Counter set to: ["+str(counter)+"] (Required Boolean Value) Defaulting to False")
		counter = -1

	while True:
		dir = os.listdir(src)
		new_dir = True

		for item in dir:
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
			src = dir_list.pop()
	
	return file_list

def main():
	dst = "./test/"
	src = "./test/"

	# rem_all_links(dst)
	src = os.path.abspath(src)
	dst = os.path.abspath(dst)
	file_list = find(get_dir_path(src), get_dir_path(dst), True)
	for file in file_list:
		print(file)

if __name__ == "__main__":
	main()
