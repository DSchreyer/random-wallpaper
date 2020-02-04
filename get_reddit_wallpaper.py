#!/usr/bin/env python
"""
This is a program that downloads the top image from a reddit subreddit and stores it in a directory.
"""
# coding: utf-8

import argparse
import ctypes
import os
from sys import platform
import re
import requests
from bs4 import BeautifulSoup
# from appscript import app, mactypes


# Parse arguments into script
parser = argparse.ArgumentParser(description="Get Wallpaper from subreddit wallpaper.")
parser.add_argument("--category",
                    type=str,
                    default="top",
                    help="Category: [hot | top | new | controversial | rising]")
parser.add_argument("--directory",
                    help="Path to directory in which images should be stored")
parser.add_argument("--change_wallpaper",
                    default="True",
                    help="Change Wallpaper? ['True' | 'False']")
parser.add_argument("--subreddit",
                    default="wallpapers",
                    help="Subreddit to download top image from")
args = parser.parse_args()
subreddit = "https://www.reddit.com/r/%s" % (args.subreddit)

headers = {'User-Agent': 'Mozilla/5.0'}

if args.directory is not None:
    directory = os.path.abspath(args.directory)
else:
    directory = os.popen("pwd").read().strip()

class GetWallpaper():
    """
    Downloads and stores wallpaper image from a reddit subreddit.
    """
    def __init__(self, url):
        self.url = url
        self.href = None
        self.src = None
        self.title = None
        self.img_href = None
        self.path = None

    def get_href(self, page_link):
        """
        Download html content from reddit.

        +

        Identifies first image on subreddit.
        """
        # get html from website
        page_response = requests.get(page_link, headers=headers)
        page_content = BeautifulSoup(page_response.text, "html.parser")

        posts = page_content.find("div",
                                  {"class": "_3JgI-GOrkmyIeDeyzXdyUD _2CSlKHjH7lsjx0IpjORx14"})
        img = posts.find("img")
        href = posts.find("a").attrs["href"]

        self.href = "%s/%s" % ("https://www.reddit.com", href)
        attrs = img.attrs
        src = attrs["src"]
        self.src = src

    def get_image(self, href):
        """
        Get title name of image and remove special characters
        """
        next_page = requests.get(href, headers=headers)
        next_content = BeautifulSoup(next_page.text, "html.parser")
        # find image url
        img_a = next_content.find("div", {"class": "media-preview-content"}).find("a")
        self.img_href = img_a.attrs["href"]
        title = next_content.find("a", {"class": "title"}).text
        title = title.replace("/", "_").replace("?", "_").replace('"', "_")
        title = title.replace("*", "_").replace("\\", "_").replace("<", "_")
        title = title.replace(">", "_").replace("|", "_").replace(":", "_").replace("'", "")
        self.title = title
    def download_image(self, title, img_href, pwd):
        """
        Download image and save it in specified directory
        """
        format_img = re.search("^.*(\..+)$", img_href).group(1)
        title = (title + format_img)
        self.path = ("%s/%s" % (pwd, title))
        print("Downloaded %s and saved it in %s" % (title, self.path))

for cat in args.category.strip().split(","):
    link = "%s/%s/" % (subreddit, cat)
    print("Download image from: %s" % (link))
    post = GetWallpaper(link)

    post.get_href(link)
    post.get_image(post.href)
    post.download_image(post.title, post.img_href, directory)
    # create dir if it does not exist
    if not os.path.exists(directory):
        os.mkdir(directory)

    # download image
    if not os.path.exists(post.path):
        f = open(post.path, 'wb')
        f.write(requests.get(post.img_href).content)
        f.close()

    # change wallpaper to downloaded image
    if platform in ("linux", "linux2"):
        if args.change_wallpaper == "True":
            print(post.path)
            os.system("feh --bg-scale '%s'" % (post.path))
            print("Change wallpaper in Unix os")
            print("Changed wallpaper to: %s" % (post.path))
    # elif platform == "darwin":
    #    print("Change wallpaper in OS X")
    #    app('Finder').desktop_picture.set(mactypes.File(post.path))
    #    print("Changed wallpaper to: %s" % (post.path))
    elif platform == "win32":
        print("Change wallpaper in Windows")
        normpath = os.path.normpath(post.path)
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, normpath, 0)
        print("Changed wallpaper to: %s" % (normpath))
    else:
        print("Operating system is not recognized")
        print("Does not change the wallpaper")
