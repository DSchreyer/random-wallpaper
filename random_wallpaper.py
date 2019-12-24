#!/usr/bin/env python
# coding: utf-8
import os
import argparse
from time import sleep
from random import randint, choice
import re

parser = argparse.ArgumentParser(description="Random Wallpaper Generator.")
parser.add_argument( "--interval", default= 0,
                     type = int, help = "Time interval in minutes")
parser.add_argument( "--directory", help = "Path to directory")
args = parser.parse_args()

if args.directory is not None:
    directory = os.path.abspath(args.directory)
else:
    directory = os.popen("pwd").read().strip()
  
def change_wallpaper(dir):
    dir_files  = os.listdir(dir)
    image_format = re.compile(".*png|.*jpg|.*jpeg|.*tiff")
    images = list(filter(image_format.match, dir_files))
    if len(images) == 0:
        print("Error! No images with the format .png, .jpg, or .jpeg in the directory: %s" % (dir))
        quit()
    rand_img = choice(images)
    rand_file = "%s/%s" % (dir, rand_img)
    os.system("gsettings set org.gnome.desktop.background picture-uri 'file://%s'" % (rand_file))
    print("Changed Wallpaper to: %s" % (rand_file))

if args.interval == 0:
    change_wallpaper(directory)
elif args.interval > 0:
    while (True):
        change_wallpaper(directory)
        sleep(args.interval*60)
