import os
import magic
import argparse
import sys
import shutil

# required for magic library to identify file types
mime = magic.Magic(mime=True)

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

# find files recursively based on type
def find(src="", dst="", type="", counter=False):

	# check required parameters
	if None in [src, dst, type]:
		print("Missing required parameters in find(src,dst,type)")
		sys.exit(4)

	file_list = []
	dir_list = []

	if counter == True:
		counter = 0
	else:
		counter = -1

	while True:
		if src != dst:
			dir = os.listdir(src)
			new_dir = True

			for item in dir:
				item_path = src+item

				# if current item is a file
				if os.path.isfile(item_path):
					file_type = mime.from_file(item_path)

					# if file is of required type
					if file_type.find(type) != -1:

						# append counter to filename if option was enabled
						if counter >= 0:
							if new_dir:
								counter += 1
								new_dir = False
							file_list.append((item_path, dst+str(counter)+" "+item))
						else:
							file_list.append((item_path, dst+item))

				# if current item is a sub directory
				else:
					dir_list.append(get_dir_path(item_path))

		if len(dir_list) == 0:
			break
		else:
			src = dir_list.pop()

	return file_list

# read user args
def read_args():

	app_desc = """A recursive file manupulation app based on file MIME type.
	Similar to a unix wildcard operation, but not depended on file extention.
	Example, if you want to copy/move all music files from one location to another,
		but you have mp3s and aac. In unix you would have to know the extention and use wildcard with
		known extension like '*.mp3' or '*.acc'. This app will instead analyze the MIME of the file
		and determine it's type even if it has no extension."""

	parser = argparse.ArgumentParser(description=app_desc)

	parser.add_argument("-V", "--version", help="show program version", action="store_true")
	parser.add_argument('-c', '--copy', help='Copy files', action="store_true")
	parser.add_argument('-m', '--move', help='Move files', action="store_true")
	parser.add_argument('-l', '--link', help='Symbolic link files', action="store_true")
	parser.add_argument('-p', '--print', help='Print to screen', action='store_true')
	parser.add_argument("-s", "--source", help="The source directory to search in", required=True)
	parser.add_argument("-d", "--destination", help="The destination directory to [copy|move|link] files to")
	parser.add_argument("-t", "--type", help="File type to search: [audio|video|python|etc]", required=True)
	parser.add_argument('--serialize', '--counter', help='Appends a counter suffix to each file per sub-directory. (Helps with grouping)', default=False, action="store_true")

	args = parser.parse_args()

	if args.version:
		print("exfile version: 0.1")
		sys.exit(0)

	# verify file operation choice
	op_choices = []
	if args.copy:
		op_choices.append('copy')
	if args.move:
		op_choices.append('move')
	if args.link:
		op_choices.append('link')
	if args.print:
		op_choices.append('print')
	if len(op_choices) != 1:
		print("Error: 0 or > 1 file operation provided. Choose between [copy|move|link|print]")
		sys.exit(3)

	# verify srouce directory exists
	if not os.path.isdir(get_dir_path(os.path.abspath(args.source))):
		print(f"Source: [{get_dir_path(os.path.abspath(args.source))}] is not a valid directory")
		sys.exit(1)

	# store values to return
	arg_dict = {
		'src': get_dir_path(os.path.abspath(args.source)),
		'type': args.type,
		'counter': args.serialize,
		'op': op_choices.pop(),
		'dst': ""
	}

	# if print only, return
	if arg_dict['op'] == 'print':
		return arg_dict

	# ELSE verify destination directory exists (else create it)
	elif arg_dict['op'] != 'print' and args.destination:
		dst = get_dir_path(os.path.abspath(args.destination))
		if not os.path.isdir(dst):
			print(f"Destination: [{dst}] is not a valid directory")
			response = input("Do you want to create it? ").lower()
			if response == 'y' or response == 'yes':
				try:
					os.makedirs(dst)

					# this is to make sure the trailing '/' after path to dir
					# is present after creating a non-existing directory
					arg_dict['dst'] = get_dir_path(os.path.abspath(args.destination))

				except FileExistsError:
					print("Error: Cannot create directory since a file already exists with that name")
					sys.exit(2)
			else:
				print("Quitting...")
				sys.exit(0)
		else:
			arg_dict['dst'] = dst
	else:
		print("Missing destination path. [(-d | --destination) /path/to/dir/]")
		sys.exit(5)
	
	return arg_dict

# main
def main():

	# read user arguments
	args = read_args()
	src = args['src']
	dst = args['dst']
	type = args['type']
	file_op = args['op']
	serialize = args['counter']

	# rem_all_links(dst)
	
	file_list = find(src, dst, type, serialize)

	print(f"""Found: [{len(file_list)}] items in [{src}]
	Performing [{file_op}] task on them to [{dst}]""")

	for file_src, file_dst in file_list:
		if file_op == 'print':
			print(file_src)
		if file_op == 'link':
			try:
				os.symlink(file_src, file_dst)
				print(f"Symbolic Linked: {file_src}")
			except(FileExistsError):
				# file exists
				print(f"Symbolic Link Exists in Destination [Skipping]: {file_src}")
				continue
		if file_op == 'move':
			shutil.move(file_src, file_dst)
			print(f"Moved: {file_src}")
		if file_op == 'copy':
			shutil.copy2(file_src, file_dst)
			print(f"Copied: {file_src}")


if __name__ == "__main__":
	main()
