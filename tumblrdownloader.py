#!/usr/bin/env python

'''
	Diego Martins de Siqueira
	download all images from a Tumblr
'''

from __future__ import unicode_literals

try:
    from urllib.request import urlopen, urlretrieve
except ImportError:
    from urllib2 import urlopen, urlretrieve

import re
import os
import sys
import argparse
import threading
from queue import Queue

class DownloadThread(threading.Thread):
    def __init__(self, queue, destfolder, image_prefix):
        super(DownloadThread, self).__init__()

        self.queue 			= queue
        self.destfolder 	= destfolder
        self.image_prefix 	= image_prefix
        self.daemon 		= True

    def run(self):
        while True:
            url = self.queue.get()
            try:
                self.download_url(url)
            except Exception as e:
                print("   Error: %s"%e)
            self.queue.task_done()

    def download_url(self, url):
        image_name = url.split('/')[-1]
        name = self.image_prefix + "_" + image_name
        dest = os.path.join(self.destfolder, name)
        print("[%s] Downloading %s"%(self.ident, image_name))
        urlretrieve(url, dest)

class TumblrDownloader:

	api_url	= 'http://#subdomain#.tumblr.com/api/read?type=photo&num=#chunk#&start=#start#' 

	def __init__(self, subdomain, chunk, output, resolution, tagged, chrono, total, start, threads):
		self._subdomain = subdomain
		self._chunk 	= chunk
		self._output 	= output
		self._resolution = resolution
		self._tagged 	= tagged
		self._chrono 	= chrono
		self._total 	= total
		self._start		= start
		self._threads	= threads

		self.api_url = self.api_url.replace("#subdomain#",self._subdomain)
		self.api_url = self.api_url.replace("#chunk#",str(self._chunk))

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

		while True:
			imagelist	=	self._getimages()
			self._start += 	self._chunk

			if not imagelist:
				break

			if self._total:
				imagelist = imagelist[0:self._total]

			self._downloadimage(imagelist)

			if self._total:
				self._total -= len(imagelist);

				if (self._total <= 0):
					break

	def _getimages(self):
		'''
			Get all images returned by Tumblr API
		'''
		site = self.api_url.replace("#start#",str(self._start))

		file = urlopen(site)
		data = file.read()
		file.close()

		regex		= r"<photo-url max-width=\"" + str(self._resolution) + "\">(.+?)</photo-url>"
		imagelist	= re.findall(regex, data)
		return imagelist

	def _downloadimage(self,url_list):
		'''
			Download a image to subdomain folder.
		'''
		queue = Queue()
		for url in url_list:
			queue.put(url)

		for i in range(self._threads):
			t = DownloadThread(queue, self._folder_path, self._image_prefix)
			t.start()

		queue.join()

def main(argv):
	parser = argparse.ArgumentParser(description="Download all images from a Tumblr")
	parser.add_argument("subdomain", type=str, 
		help="Tumblr subdomain you want to download")
	parser.add_argument("--chunk", type=int, default=20, 
		help="The number of posts to return each call to Tumblrs API. The default is 20, and the maximum is 50.")
	parser.add_argument("--total", type=int,
		help="Total images to download")
	parser.add_argument("--start", type=int, default=0, 
		help="The post offset to start from. The default is 0.")
	parser.add_argument("--output", type=str, default="images", 
		help="Output folder")
	parser.add_argument("--resolution", type=int, default=1280, choices=[1280, 500, 400, 250, 100, 75],
        help="Select Max Width to download. The default is 1280.")
	parser.add_argument("--tagged", type=str,
		help="Download only images with tag")
	parser.add_argument("--chrono", action="store_true", 
		help="Sort in chronological order (oldest first)")
	parser.add_argument("--threads", type=int, default=5, 
		help="Number of parallel downloads. The default is 5.")

	args = parser.parse_args()

	print('Downloading Subdomain: ', args.subdomain)

	try:
		td = TumblrDownloader(args.subdomain,args.chunk,args.output,args.resolution,args.tagged,args.chrono,
			args.total,args.start,args.threads)
		td.download()
		print('All images were downloaded.')
	except KeyboardInterrupt:
		print('Interrupt received, stopping downloads')

	sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
