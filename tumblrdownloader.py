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

class TumblrDownloader:

	api_url	= 'http://#subdomain#.tumblr.com/api/read?type=photo&num=#chuck#&start=#start#' 

	def __init__(self, subdomain, chuck, output, resolution, tagged, chrono):
		self._subdomain = subdomain
		self._chuck = chuck
		self._output = output
		self._resolution = resolution
		self._tagged = tagged
		self._chrono = chrono

		self.api_url = self.api_url.replace("#subdomain#",self._subdomain)
		self.api_url = self.api_url.replace("#chuck#",str(self._chuck))

		self._image_prefix = self._subdomain;

		self._folder_path = self._output + "/" + self._subdomain + "/" + str(self._resolution)

		if (self._chrono):
			self.api_url += "&chrono=1"

		if self._tagged:
			self.api_url 		+= "&tagged=" + self._tagged
			self._folder_path 	+= "/" + self._tagged
			self._image_prefix	+= "_" + self._tagged;

		self._createfolder()

	def _createfolder(self):
		'''
			if folder does not exist, create it.
		'''

		if not os.path.exists(self._folder_path):
	 		os.makedirs(self._folder_path)

	def download(self):
		'''
			download all images from a Tumblr
		'''

		start = 0

		while True:
			imagelist = self._getimages(start)
			start     = start + self._chuck

			if not imagelist:
				break

			for image in imagelist:
				self._downloadimage(image)

	def _getimages(self, start):
		'''
			Get all images returned by Tumblr API
		'''
		site = self.api_url.replace("#start#",str(start))

		file = urllib2.urlopen(site)
		data = file.read()
		file.close()

		regex		= ur"<photo-url max-width=\"" + str(self._resolution) + "\">(.+?)</photo-url>"
		imagelist	= re.findall(regex, data)
		return imagelist

	def _downloadimage(self,url):
		'''
			Download a image to subdomain folder.
		'''
		file_name 	= self._image_prefix + "_" + url.split('/')[-1]

		u 			= urllib2.urlopen(url)
		f 			= open(self._folder_path + "/" + file_name, 'wb')
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

def main(argv):
	parser = argparse.ArgumentParser(description="Download all images from a Tumblr")
	parser.add_argument("subdomain", type=str, 
		help="Tumblr subdomain you want to download")
	parser.add_argument("--chuck", type=int, default=50, 
		help="The number of posts to return each call to Tumblrs API")
	parser.add_argument("--output", type=str, default="images", 
		help="Output folder")
	parser.add_argument("--resolution", type=int, default=1280, choices=[1280, 500, 400, 250, 100, 75],
        help="Select Max Width to download")
	parser.add_argument("--tagged", type=str,
		help="Download only images with tag")
	parser.add_argument("--chrono", action="store_true", 
		help="Sort in chronological order (oldest first)")

	args = parser.parse_args()

	print 'Downloading Subdomain: ', args.subdomain

	try:
		td = TumblrDownloader(args.subdomain,args.chuck,args.output,args.resolution,args.tagged,args.chrono)
		td.download()
		print 'All images were downloaded.'
	except KeyboardInterrupt:
		print 'Interrupt received, stopping downloads'

	sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
