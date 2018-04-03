import os
import shutil
import subprocess
from tkinter import *
from tkinter import ttk, filedialog, messagebox

class CaptionSort:

    def sort_callback(self):
        #create an empty list to store the file paths as you examine them
        image_paths = []
        # make a 3-element tuple when you start taking the source directory and walk along it, with dirpath:
        #being the name of the directory you are in, dirnames:being the names of all subdirectories in the dirpath, and
        #filenames:being file names that are in the dirpath directory
        for dirpath, dirnames, filenames in os.walk(self.src_entry.get()):
            for file in filenames:
                if file.endswith(('.jpg','.png')):
                    #since the filename doesn't have a complete path, try to create a path for the filename by joining the
                    #dirpath with the filename
                    image_paths.append(os.path.join(dirpath, file))

        sort_dirs = {}
        for key in range(ord('A'), ord('Z')+1):
            sort_dirs[chr(key)] = []

        for path in image_paths:
            if path.endswith('.jpg'):
                tag = '-Caption-Abstract'
            elif path.endswith('.png')
                tag = '-Description'
            try: # use ExifTool from http://www.sno.phy.queensu.ca/~phil/exiftool/
                output = subprocess.check_output(['exiftool', tag, path])
                caption = output.decode(encoding = 'utf_8')[34:].rstrip()
            except:
                print('Error getting Exif data for ' + path)
            else:
                print('Caption found for {} - {}'.format(path, caption))
                if caption:
                    try: # will fail if caption does not begin with a letter
                        sort_dirs[caption[0].upper()].append(path)
                    except:
                        print('Error sorting {} - Caption begins with {}'.format(path, caption[0]))

        sorted_count = 0
        for key in sort_dirs.keys():
            if sort_dirs[key]:
                keypath = os.path.join(self.dest_entry.get(), key)
                if not os.path.exists(keypath):
                    try:
                        os.makedirs(keypath)
                    except os.error as e:
                        print (str(e))
                for file in sort_dirs[key]:
                    if self.copy_var.get():
                        try:
                            shutil.copy(file, os.path.join(keypath, file.split('/')[-1]))
                        except IOError as e:
                            print(str(e))
                        else:
                            print('Copied {} to {}'.format(file, keypath))
                            sorted_count += 1
                    else:
                        try:
                            shutil.move(file, os.path.join(keypath, file.split('/')[-1]))
                        except IOError as e:
                            print(str(e))
                        else:
                            print('Moved {} to {}'.format(file, keypath))
                            sorted_count += 1
