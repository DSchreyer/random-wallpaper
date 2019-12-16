#!/usr/bin/env python
# coding: utf-8
import os
import argparse
from time import sleep
from random import randint

parser = argparse.ArgumentParser(description="Random Wallpaper Generator.")
parser.add_argument( "--interval", default= 0,
                     type = int, help = "Time interval in minutes")
parser.add_argument( "--dir", help = "Path to directory")
args = parser.parse_args()

def change_wallpaper(dir):
    b = len(os.listdir(dir)) - 1
    r = randint(a=0, b=b)
    rand_img = os.listdir(dir)[r]
    rand_file = "%s/%s" % (dir, rand_img)
    print("Changed Wallpaper to: %s" % (rand_file))
    rand_file_full = "file://%s" % (rand_file)
    os.system("gsettings set org.gnome.desktop.background picture-uri '%s'" % (rand_file_full))
if args.interval == 0:
    change_wallpaper(args.dir)
elif args.interval > 0:
    while (True):
        change_wallpaper(args.dir)
        sleep(args.interval*60)
