# random-wallpaper
Chooses a random image file from a directory and sets it as your wallpaper.

## get-reddit-wallpaper
Downloads first top|hot|rising|new|controversial wallpaper from the subreddit wallpapers into a specific directory.

### Usage
``` bash
Usage: get_reddit_wallpaper.py --option <argument>

get_reddit_wallpaper.py --directory <Path-to-directory> [--category <(cat1|cat1,cat2,..)>] [--change_wallpaper <("True"|"False")>]
```

category: Sorting category on reddit. Defaul: "top". Optional: "hot", "rising", "new", "top", "controversial".
          Multiple categories are also possible: e.g. top,hot,rising
