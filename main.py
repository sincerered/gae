# Copyright 2012 Google Inc. All Rights Reserved.


"""A sample app that uses GCS client to operate on bucket and file."""
import datetime
import logging
import os
import cloudstorage as gcs
import webapp2
import sys
import urllib

from google.appengine.api import app_identity

my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)


class MainPage(webapp2.RequestHandler):
  """Main page for GCS demo application."""

  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write("start\n")
    if os.path.isfile(sys.path[0] + "/Bucket/option_data/20150323"):
      self.respones.write('kerker')


    self.response.write(os.listdir(sys.path[0]))

    url = "http://www.taifex.com.tw/DailyDownload/"

    downloadurl = url + "/Daily_2015_03_24.zip"

    self.response.write(gcs.listbucket())

    #urllib.urlretrieve(downloadurl, sys.path[0] + "/Daily_2015_03_24.zip")

      
# When writing a file to Cloud Storage, you should not call finally:close() as
# this can result in finalizing object uploads even if there was an exception
# during a write.
  def create_file(self, filename):
    """Create a file.

    The retry_params specified in the open call will override the default
    retry params for this particular file handle.

    Args:
      filename: filename.
    """
    self.response.write('Creating file %s\n' % filename)

    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(filename,
                        'w',
                        content_type='text/plain',
                        options={'x-goog-meta-foo': 'foo',
                                 'x-goog-meta-bar': 'bar'},
                        retry_params=write_retry_params)
    gcs_file.write('abcde\n')
    gcs_file.write('f'*1024*4 + '\n')
    gcs_file.close()
    self.tmp_filenames_to_clean_up.append(filename)

  def read_file(self, filename):
    self.response.write('Abbreviated file content (first line and last 1K):\n')

    gcs_file = gcs.open(filename)
    self.response.write(gcs_file.readline())
    gcs_file.seek(-1024, os.SEEK_END)
    self.response.write(gcs_file.read())
    gcs_file.close()

  def stat_file(self, filename):
    self.response.write('File stat:\n')

    stat = gcs.stat(filename)
    self.response.write(repr(stat))

  def create_files_for_list_bucket(self, bucket):
    self.response.write('Creating more files for listbucket...\n')
    filenames = [bucket + n for n in ['/foo1', '/foo2', '/bar', '/bar/1',
                                      '/bar/2', '/boo/']]
    for f in filenames:
      self.create_file(f)

  def list_bucket(self, bucket):
    """Create several files and paginate through them.

    Production apps should set page_size to a practical value.

    Args:
      bucket: bucket.
    """
    self.response.write('Listbucket result:\n')

    page_size = 1
    stats = gcs.listbucket(bucket + '/foo', max_keys=page_size)
    while True:
      count = 0
      for stat in stats:
        count += 1
        self.response.write(repr(stat))
        self.response.write('\n')

      if count != page_size or count == 0:
        break
      stats = gcs.listbucket(bucket + '/foo', max_keys=page_size,
                             marker=stat.filename)

  def list_bucket_directory_mode(self, bucket):
    self.response.write('Listbucket directory mode result:\n')
    for stat in gcs.listbucket(bucket + '/b', delimiter='/'):
      self.response.write('%r' % stat)
      self.response.write('\n')
      if stat.is_dir:
        for subdir_file in gcs.listbucket(stat.filename, delimiter='/'):
          self.response.write('  %r' % subdir_file)
          self.response.write('\n')

  def delete_files(self):
    self.response.write('Deleting files...\n')
    for filename in self.tmp_filenames_to_clean_up:
      self.response.write('Deleting file %s\n' % filename)
      try:
        gcs.delete(filename)
      except gcs.NotFoundError:
        pass

class taskspr(webapp2.RequestHandler):
  def get(self):

    date = datetime.datetime.now()
    date = date.strftime("%Y%m%d%H%M")
    bucket = "/option_data"
    datefilename = bucket + "/" + date
    self.create_file(datefilename)

  def create_file(self, filename):
    """Create a file.

    The retry_params specified in the open call will override the default
    retry params for this particular file handle.

    Args:
      filename: filename.
    """
    self.response.write('Creating file %s\n' % filename)

    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(filename,
                        'w',
                        content_type='text/plain',
                        options={'x-goog-meta-foo': 'foo',
                                 'x-goog-meta-bar': 'bar'},
                        retry_params=write_retry_params)
    gcs_file.write('abcde\n')
    gcs_file.write('f'*1024*4 + '\n')
    gcs_file.close()
    self.tmp_filenames_to_clean_up.append(filename)

  def read_file(self, filename):
    self.response.write('Abbreviated file content (first line and last 1K):\n')

    gcs_file = gcs.open(filename)
    self.response.write(gcs_file.readline())
    gcs_file.seek(-1024, os.SEEK_END)
    self.response.write(gcs_file.read())
    gcs_file.close()

  def stat_file(self, filename):
    self.response.write('File stat:\n')

    stat = gcs.stat(filename)
    self.response.write(repr(stat))

  def create_files_for_list_bucket(self, bucket):
    self.response.write('Creating more files for listbucket...\n')
    filenames = [bucket + n for n in ['/foo1', '/foo2', '/bar', '/bar/1',
                                      '/bar/2', '/boo/']]
    for f in filenames:
      self.create_file(f)

  def list_bucket(self, bucket):
    """Create several files and paginate through them.

    Production apps should set page_size to a practical value.

    Args:
      bucket: bucket.
    """
    self.response.write('Listbucket result:\n')

    page_size = 1
    stats = gcs.listbucket(bucket + '/foo', max_keys=page_size)
    while True:
      count = 0
      for stat in stats:
        count += 1
        self.response.write(repr(stat))
        self.response.write('\n')

      if count != page_size or count == 0:
        break
      stats = gcs.listbucket(bucket + '/foo', max_keys=page_size,
                             marker=stat.filename)

  def list_bucket_directory_mode(self, bucket):
    self.response.write('Listbucket directory mode result:\n')
    for stat in gcs.listbucket(bucket + '/b', delimiter='/'):
      self.response.write('%r' % stat)
      self.response.write('\n')
      if stat.is_dir:
        for subdir_file in gcs.listbucket(stat.filename, delimiter='/'):
          self.response.write('  %r' % subdir_file)
          self.response.write('\n')

  def delete_files(self):
    self.response.write('Deleting files...\n')
    for filename in self.tmp_filenames_to_clean_up:
      self.response.write('Deleting file %s\n' % filename)
      try:
        gcs.delete(filename)
      except gcs.NotFoundError:
        pass

class Option(webapp2.RequestHandler):
  def get(self):
    self.response.write("option")
    





app = webapp2.WSGIApplication([('/', MainPage),('/getoption', Option)],
                              debug=True)
