# TumblrDownloader
Download all imagens from a Tumblr

## Screenshots

<img src="preview/demo.png" alt="Start download" width="100%"/>
<img src="preview/demo2.png" alt="All images were downloaded" width="100%"/>

## Requirements

* [Python](https://www.python.org)

## Command line syntax

```bash
python tumblrdownloader.py -s <subdomain> -t <chunck>
```
Tumblr: http://bibliammo.tumblr.com/

###example 1
```bash
 tumblrdownloader.py -s bibliammo
```
###example 2
```bash
 tumblrdownloader.py -s bibliammo -c 10
```

## Find a bug/issue or simply want to request a new feature?

[Create a Github issue/feature request!](https://github.com/DiSiqueira/TumblrDownloader/issues/new)

## Upcoming features

* Asynchronous downloads
* Resume download
* Limit total downloads