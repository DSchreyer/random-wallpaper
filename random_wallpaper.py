#!/usr/bin/env python
"""
Randomly changes the background to an image file in a given directory.

Supports continues wallpaper change every x minutes.
"""
# coding: utf-8
import os
import argparse
from time import sleep
from random import choice
import re

PARSER = argparse.ArgumentParser(description="Random Wallpaper Generator.")
PARSER.add_argument("--interval", default=0,
                    type=int, help="Time interval in minutes")
PARSER.add_argument("--directory", help="Path to directory")
ARGS = PARSER.parse_args()

if ARGS.directory is not None:
    DIRECTORY = os.path.abspath(ARGS.directory)
else:
    DIRECTORY = os.popen("pwd").read().strip()

def change_wallpaper(d):
    """
    Changes the background to a random image in a directory.
    """
    dir_files = os.listdir(d)
    image_format = re.compile(".*png|.*jpg|.*jpeg|.*tiff")
    images = list(filter(image_format.match, dir_files))
    if not images:
        print("Error! No images with the format .png, .jpg, or .jpeg in the directory: %s" % (d))
        quit()
    rand_img = choice(images)
    rand_file = "%s/%s" % (d, rand_img)
    os.system("feh --bg-scale '%s'" % (rand_file))
    print("Changed Wallpaper to: %s" % (rand_file))

if ARGS.interval == 0:
    change_wallpaper(DIRECTORY)
elif ARGS.interval > 0:
    while True:
        change_wallpaper(DIRECTORY)
        sleep(ARGS.interval*60)
