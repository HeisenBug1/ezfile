import os
import magic
import argparse
import sys

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
def find(src, dst, counter=False):
    file_list = []
    dir_list = []

    if counter == True:
        counter = 0
    else:
        print("Counter set to: ["+str(counter) +
              "] (Required Boolean Value) Defaulting to False")
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
    parser.add_argument('--copy', help='Copy files')
    parser.add_argument('--move', help='Move files')
    parser.add_argument('--link', help='Symbolic link files')
    parser.add_argument("-s", "--source", help="The source directory to search in", required=True)
    parser.add_argument("-d", "--destination", help="The destination directory to [copy|move|link] files to", required=True)
    parser.add_argument("-t", "--type", help="File type to search: [audio|video|python|etc]", required=True)
    parser.add_argument('--serialize', '--counter', help='Appends a counter suffix to each file per sub-directory. (Helps with grouping)', default=False, action="store_true")

    args = parser.parse_args()

    if args.version:
        print("exfile version: 0.1")
        sys.exit(0)

    # verify file operation choice
    op_choices = []
    if args.copy:
        op_choices.append('cp')
    if args.move:
        op_choices.append('mv')
    if args.link:
        op_choices.append('ln -s')
    if len(op_choices) != 1:
        print("Error: 0 or > 1 file operation provided. Choose between [copy|move|link]")
        sys.exit(3)

    # verify srouce directory exists
    if not os.path.isdir(args.src):
        print("Source: ["+args.src+"] is not a valid directory")
        sys.exit(1)

    # verify destination directory exists (else create it)
    if not os.path.isdir(args.dst):
        print(f"Destination: [{args.dst}] is not a valid directory")
        response = input("Do you want to create it? ").lower()
        if response == 'y' or response == 'yes':
            try:
                os.makedirs(get_dir_path(args.dst))
            except FileExistsError:
                print("Error: Cannot create directory since a file already exists with that name")
                sys.exit(2)
        else:
            sys.exit(0)

    arg_dict = {
        'src': args.src,
        'dst': args.dst,
        'type': args.type,
        'counter': args.counter,
        'op': op_choices.pop()
    }

    return arg_dict

# main
def main():

    # read user arguments
    args = read_args()

    # dst = "./test/"
    # src = "./test/"

    # rem_all_links(dst)
    # src = os.path.abspath(src)
    # dst = os.path.abspath(dst)
    # file_list = find(get_dir_path(src), get_dir_path(dst), True)
    # for file in file_list:
    # 	print(file)


if __name__ == "__main__":
    main()
