import boto
import os
import json

S3_LOCATION = 'us-west-1'
BUCKET_NAME = 'alexa-website'
DEST_BUCKET_NAME = 'alexa-website1494005721768'

def alexa_s3_website_create(event,context):
    print event
    body = event['body']
    background_value = ''
    border_value = ''
    key_value = body.split(',')
    action = key_value[0]
    value = key_value[1]
    access_key=os.environ['aws_access_key_id']
    secret_key=os.environ['aws_secret_access_key']
    # access_key = 'AKIAJZRFLFT2F6M5YNOQ'
    # secret_key = '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'
    conn = boto.s3.connect_to_region(S3_LOCATION,aws_access_key_id=access_key,aws_secret_access_key=secret_key)

    if action == 'change-background':
        background_value = value + '.jpg'

    if action == 'change-border':
        border_value = value

    index_html = """
        <html>
            <head><title>Pairing Alexa</title>
            <script language="JavaScript" type="text/javascript">
            setTimeout("location.href='index.html'",10000 )
          </script>
            </head>
          <body style="background-image: url('{background_value}'); border-style: {border_value} ">
            <center><h1>Hello! I am Alexa :)</h1></center>
          </body>
        </html>
    """.format(background_value=background_value,border_value=border_value)

    error_html = """
    <html>
      <head><title>Something is wrong</title></head>
      <body><h2>Something is terribly wrong with my S3-based website</h2></body>
    </html>"""
    #to create bucket
    # website_bucket = conn.create_bucket(BUCKET_NAME,
    #                                     location=S3_LOCATION,
    #                                     policy='public-read')

    # to access bucket
    src_website_bucket = conn.get_bucket(BUCKET_NAME)

    index_key = src_website_bucket.new_key('index.html')
    index_key.content_type = 'text/html'
    index_key.set_contents_from_string(index_html, policy='public-read')

    website_bucket = conn.get_bucket(DEST_BUCKET_NAME)
    for k in website_bucket.list():
        k.delete


    for k in src_website_bucket.list():
        website_bucket.copy_key(k.key, BUCKET_NAME, k.key)
        website_bucket.set_acl('public-read',k.key)
    website_bucket.set_acl('public-read','index.html')
    website_bucket.set_acl('public-read','dog.jpg')
    website_bucket.set_acl('public-read','cat.jpg')

    # error_key = website_bucket.new_key('error.html')
    # error_key.content_type = 'text/html'
    # error_key.set_contents_from_string(error_html, policy='public-read')

    # now set the website configuration for our bucket
    website_bucket.configure_website('index.html', 'error.html')


    # now get the website configuration, just to check it
    # return 'http://'+DEST_BUCKET_NAME+'.s3-website-'+S3_LOCATION+'.amazonaws.com/'

    return {"isBase64Encoded": 'false',
    "statusCode": 200,
    "headers": {},
    "body": '{"url":"http://'+DEST_BUCKET_NAME+'.s3-website-'+S3_LOCATION+'.amazonaws.com/"}'
             }

# alexa_s3_website_create('{"body": "change-border,solid"}','')