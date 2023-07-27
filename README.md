# ezfile
 A recursive file manupulation app based on file MIME type.<br>
 Similar to a unix wildcard operation, but not depended on file extention.
 
 Example, if you want to copy/move all music files from one location to another, but you have mp3s and aac. In Linux/Mac you would have to know the extention and use wildcards each time with known extension like '*.mp3' or '*.acc' even though they are both audio types. This app will instead analyze the MIME of the file and determine it's type even if it has no extension and perform operations like copy, move, delete, symlink, etc with ease.

 Linux: `sudo apt-get install libmagic1`<br>
 Mac: `brew install libmagic`<br>
 Windows: `pip install python-magic-bin`
