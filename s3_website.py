import boto
from boto.s3.connection import Location
import time
millis = int(round(time.time() * 1000))

S3_LOCATION = 'us-west-1'
BUCKET_NAME = 'alexa-website'
DEST_BUCKET_NAME = 'alexa-website1494005721768'

conn = boto.s3.connect_to_region(S3_LOCATION)

error_html = """
<html>
  <head><title>Something is wrong</title></head>
  <body><h2>Something is terribly wrong with my S3-based website</h2></body>
</html>"""
#to create bucket
# website_bucket = conn.create_bucket(BUCKET_NAME,
#                                     location=S3_LOCATION,
#                                     policy='public-read')

website_bucket = conn.get_bucket(DEST_BUCKET_NAME)
for k in website_bucket.list():
    k.delete
#to access bucket
src_website_bucket = conn.get_bucket(BUCKET_NAME)

for k in src_website_bucket.list():
    website_bucket.copy_key(k.key, BUCKET_NAME, k.key)
website_bucket.set_acl('public-read','index.html')
# index_key = website_bucket.new_key('index.html')
# index_key.content_type = 'text/html'
# index_key.set_contents_from_filename('/Users/kanthivel/Desktop/index.html', policy='public-read')
# error_key = website_bucket.new_key('error.html')
# error_key.content_type = 'text/html'
# error_key.set_contents_from_string(error_html, policy='public-read')

# now set the website configuration for our bucket
website_bucket.configure_website('index.html', 'error.html')


# now get the website configuration, just to check it
print website_bucket.get_website_configuration()
print 'http://'+DEST_BUCKET_NAME+'.s3-website-'+S3_LOCATION+'.amazonaws.com/'
