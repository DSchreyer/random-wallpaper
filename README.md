# random-wallpaper
Chooses a random image file from a directory and sets it as your wallpaper.

## get-reddit-wallpaper
Downloads first top|hot|rising|new|controversial image from an individual subreddit into a specific directory. Optimal for downloading wallpapers and combine it with the random-wallpaper generator. Download every day top wallpapers from reddit and set them as your background.

### Usage
``` bash
get_reddit_wallpaper.py [--directory <Path-to-directory>] [--category <>] [--change_wallpaper <True/False>]
```

category: Sorting category on reddit. Default: "top". Optional: "hot", "rising", "new", "top", "controversial".
          Multiple categories are also possible: For example: "top,hot,rising"
