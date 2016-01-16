#!/usr/bin/env python

'''
	Diego Martins de Siqueira
	download all images from a Tumblr
'''

import urllib2
import re
import os
import sys
import argparse


API_URL = "http://#subdomain#.tumblr.com/api/read?type=photo&num=#chunck#&start=#start#"

def createfolder(name):
	'''
		if folder does not exist, create it.
	'''
	if not os.path.exists(name):
 		os.makedirs(name)

def downloadimage(url,subdomain,output):
	'''
		Download a image to subdomain folder.
	'''
	file_name 	= subdomain + "_" + url.split('/')[-1]
	folder_path = output + "/" + subdomain

	createfolder(folder_path)

	u 			= urllib2.urlopen(url)
	f 			= open(folder_path + "/" + file_name, 'wb')
	meta 		= u.info()
	file_size 	= int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_name, file_size)

	file_size_dl 	= 0
	block_sz		= 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break

	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print status,

	f.close()

def getimages(site,start,chunck):
	'''
		Get all images returned by Tumblr API
	'''
	site = site.replace("#chunck#",str(chunck))
	site = site.replace("#start#",str(start))
	file = urllib2.urlopen(site)
	data = file.read()
	file.close()
	regex		= ur"<photo-url max-width=\"1280\">(.+?)</photo-url>"
	imagelist	= re.findall(regex, data)
	return imagelist

def finish():
	'''
		Finish message
	'''
	print 'All images were downloaded.'
	sys.exit()

def download(subdomain,chunck,output):
	'''
		download all images from a Tumblr
	'''
	site  = API_URL.replace("#subdomain#",subdomain)
	start = 0

	while True:
		imagelist = getimages(site,start,chunck)
		start     = start + chunck

		if not imagelist:
			finish()

		for image in imagelist:
			downloadimage(image,subdomain,output)

def help(error):
	'''
		Print help message
	'''
	if (error > 0):
		print 'Error:', error
		print ''
	print 'tumblrdownloader.py -s <subdomain> -t <chunck> -o <output>'
	print 'Tumblr: http://bibliammo.tumblr.com/'
	print 'example: tumblrdownloader.py -s bibliammo'
	print 'example: tumblrdownloader.py -s bibliammo -c 10'
	print 'example: tumblrdownloader.py -s bibliammo -o allimages'
	sys.exit(error)

def main(argv):
	parser = argparse.ArgumentParser(description="Download all images from a Tumblr")
	parser.add_argument("subdomain", type=str, 
		help="Tumblr subdomain you want to download")
	parser.add_argument("--chuck", type=int, default=50, 
		help="The number of posts to return each call to Tumblrs API")
	parser.add_argument("--chrono", action="store_true", 
		help="Sort in chronological order (oldest first)")
	parser.add_argument("--resolution", type=int, default=1280, choices=[1280, 500, 400, 250, 100, 75],
        help="Select Max Width to download")
	parser.add_argument("--output", type=str, default="images", 
		help="Output folder")
	parser.add_argument("--tagged", type=str,
		help="Download only images with tag")

	args = parser.parse_args()

	print 'Downloading Subdomain: ', args.subdomain

	try:
		download(args.subdomain,args.chuck,args.output)
	except KeyboardInterrupt:
		print 'Interrupt received, stopping downloads'

if __name__ == "__main__":
   main(sys.argv[1:])
