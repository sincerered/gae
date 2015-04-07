# Copyright 2012 Google Inc. All Rights Reserved.

import datetime
import logging
import os
import cloudstorage as gcs
import webapp2
import sys
#import urllib2

from google.appengine.api import app_identity




class MainPage(webapp2.RequestHandler):
  """Main page for GCS demo application."""
  def get(self):
    
"""		try:
			url = urllib2.urlopen("http://info512.taifex.com.tw/Future/FusaQuote_Norl.aspx?d=3000300").read().decode("utf-8")

			x = etree.HTML(url).xpath(
				'//span[@id="ctl00_ContentPlaceHolder1_uc_DgFusaQuote1_dgData_ctl03_lblItemStatus"]/parent::font/parent::td/following-sibling::td/font')
		except:
			self.response.write("error")
		else:	
			for i in x:
				self.response.write("{}\t".format(i.text))
"""
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write("kerker")		

#kkkk  

app = webapp2.WSGIApplication([('/getminutedata', MainPage)],
                              debug=True)

