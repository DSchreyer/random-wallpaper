#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import re
import os
import argparse

# Parse arguments into script
parser = argparse.ArgumentParser(description="Get Wallpaper from subreddit wallpaper.")
parser.add_argument( "--category",
                     type=str,
                     default = "top",
                     help = "Category: [hot | top | new | controversial | rising]")
parser.add_argument( "--directory",
                     default="./",
                     help = "Path to directory in which images should be stored")
parser.add_argument( "--change_wallpaper",
                     default= "True",
                     help = "Change Wallpaper? ['True' | 'False']")
args = parser.parse_args()

subreddit = "https://www.reddit.com/r/wallpapers"

headers = {'User-Agent': 'Mozilla/5.0'}
directory = args.directory

class get_wallpaper():
    def __init__(self, url):
        self.url = url

    def get_href(self, page_link):
        # get html from website
        page_response = requests.get(page_link, headers=headers)
        page_content = BeautifulSoup(page_response.text, "html.parser")

        posts = page_content.find("div", {"class": "_3JgI-GOrkmyIeDeyzXdyUD _2CSlKHjH7lsjx0IpjORx14"})
        img = posts.find("img")
        href = posts.find("a").attrs["href"]

        self.href = "%s/%s" % ("https://www.reddit.com", href)
        attrs = img.attrs
        src = attrs["src"]
        self.src = src

    def get_image(self, href):
        next_page = requests.get(href, headers=headers)
        next_content = BeautifulSoup(next_page.text, "html.parser")
        # find image url
        img_a = next_content.find("div", {"class": "media-preview-content"}).find("a")
        self.img_href = img_a.attrs["href"]
        self.title = next_content.find("a", {"class": "title"}).text.replace("/", "_").replace("?", "_").replace('"',
                                                                                                                 "_")
    def download_image(self, title, img_href, pwd):
        format_img = re.search("^.*(\..*)$", img_href).group(1)
        title = (title + format_img)
        self.path = ("%s/%s" % (pwd, title))
        print("Downloaded %s and saved it in %s" % (title, self.path))

for cat in args.category.strip().split(","):
    link = "%s/%s/" % (subreddit, cat)
    post = get_wallpaper(link)

    post.get_href(link)
    post.get_image(post.href)
    post.download_image(post.title, post.img_href, directory)
    full_name = "file://%s" % (post.path)
    # create dir if it does not exist
    if not os.path.exists(directory):
        os.mkdir(directory)

    # download image
    if not os.path.exists(post.path):
        f = open(post.path,'wb')
        f.write(requests.get(post.img_href).content)
        f.close()

    # change wallpaper to downloaded image
    if args.change_wallpaper == "True":
        os.system("gsettings set org.gnome.desktop.background picture-uri '%s'" % (full_name))
        print("Changed wallpaper to: %s" % (post.path))

