# TumblrDownloader
Download all imagens from a Tumblr, in highest resolution

## Screenshots

<img src="preview/demo.png" alt="Download all images from a Tumblr" width="100%"/>

## Requirements

* [Python](https://www.python.org)

## Usage

```bash
tumblrdownloader.py [-h] [--chuck CHUCK] [--chrono]
                    [--resolution {1280,500,400,250,100,75}]
                    [--output OUTPUT] [--tagged TAGGED]
                    subdomain

Download all images from a Tumblr

positional arguments:
  subdomain             Tumblr subdomain you want to download

optional arguments:
  -h, --help            show this help message and exit
  --chuck CHUCK         The number of posts to return each call to Tumblrs API
  --chrono              Sort in chronological order (oldest first)
  --resolution {1280,500,400,250,100,75}
                        Select resolution to download
  --output OUTPUT       Output folder
  --tagged TAGGED       Download only images with tag
```
Tumblr: http://bibliammo.tumblr.com/

###Example 1
```bash
 python tumblrdownloader.py bibliammo
```
###Example 2
```bash
 python tumblrdownloader.py --chuck 10 bibliammo
```
###Example 3
```bash
 python tumblrdownloader.py --output images2 bibliammo
```
###Example 4 
```bash
 python tumblrdownloader.py --chuck 1 --output images2 --resolution 100 --chrono --tagged biblia bibliammo
```

## Find a bug/issue or simply want to request a new feature?

[Create a Github issue/feature request!](https://github.com/DiSiqueira/TumblrDownloader/issues/new)

## Upcoming features

* Asynchronous downloads
* Resume download
* Limit total downloads