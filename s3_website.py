import os

import boto
from boto.s3.key import Key

S3_LOCATION = 'us-west-1'
BUCKET_NAME = 'alexa-website'
DEST_BUCKET_NAME = 'alexa-website1494005721768'

def alexa_s3_website_create(event,context):
    PROPERTY_FILE_NAME = 'properties.txt'
    print event
    body = event['body']
    access_key = os.environ['aws_access_key_id']
    secret_key = os.environ['aws_secret_access_key']
    key_value = body.split(',')
    action = key_value[0]
    value = key_value[1]
    background_value, border_value, website_name ='','',''
    conn = boto.s3.connect_to_region(S3_LOCATION, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    src_website_bucket = conn.get_bucket(BUCKET_NAME)
    if(action == 'create-website'):
        property_key = src_website_bucket.new_key('properties.txt')
        property_key.content_type = 'text/plain'
        property_key.set_contents_from_string('', policy='public-read')
        if value == 'women who code':
            PROPERTY_FILE_NAME = 'properties1.txt'

    conn = boto.s3.connect_to_region(S3_LOCATION, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    src_website_bucket = conn.get_bucket(BUCKET_NAME)
    k = Key(src_website_bucket)
    k.key = PROPERTY_FILE_NAME
    k.open()
    properties_string = k.read()
    print properties_string
    if properties_string != '':
        properties_array = properties_string.split('\n')
        background_value, border_value, website_name = properties_array[0], properties_array[1], properties_array[2]

    if action == 'change-background':
        background_value = value + '.jpg'

    if action == 'change-border':
        border_value = value

    if action == 'create-website':
        website_name = value


    index_html = """
        <html>
            <head><title>Pairing Alexa</title>
            <script language="JavaScript" type="text/javascript">
            setTimeout("location.href='index.html'",7000 )
          </script>
            </head>
          <body style="background-color:black;background-image: url('{background_value}'); border: {border_value} white 3px; background-size:cover">
            <center><h1 style="color:white">Hello! Welcome to {website_name} :)</h1></center>
          </body>
        </html>
    """.format(background_value=background_value, border_value=border_value, website_name=website_name)

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

    index_key = src_website_bucket.new_key('index.html')
    index_key.content_type = 'text/html'
    index_key.set_contents_from_string(index_html, policy='public-read')

    property_key = src_website_bucket.new_key('properties.txt')
    property_key.content_type = 'text/plain'
    property_key.set_contents_from_string(background_value+'\n'+border_value+'\n'+website_name+'\n'+BUCKET_NAME, policy='public-read')

    website_bucket = conn.get_bucket(DEST_BUCKET_NAME)
    for k in website_bucket.list():
        k.delete


    for k in src_website_bucket.list():
        website_bucket.copy_key(k.key, BUCKET_NAME, k.key)
        website_bucket.set_acl('public-read',k.key)
    website_bucket.set_acl('public-read','index.html')
    website_bucket.set_acl('public-read','savethehacker1.jpg')
    website_bucket.set_acl('public-read','savethehacker2.jpg')
    website_bucket.set_acl('public-read','womenwhocode1.png')
    website_bucket.set_acl('public-read','womenwhocode2.jpg')
    website_bucket.set_acl('public-read','properties.txt')
    website_bucket.set_acl('public-read','properties1.txt')

    # error_key = website_bucket.new_key('error.html')
    # error_key.content_type = 'text/html'
    # error_key.set_contents_from_string(error_html, policy='public-read')

    # now set the website configuration for our bucket
    website_bucket.configure_website('index.html', 'error.html')


    # now get the website configuration, just to check it
    # return 'http://'+DEST_BUCKET_NAME+'.s3-website-'+S3_LOCATION+'.amazonaws.com/'
    print {"isBase64Encoded": 'false',
    "statusCode": 200,
    "headers": {},
    "body": '{"url":"http://'+DEST_BUCKET_NAME+'.s3-website-'+S3_LOCATION+'.amazonaws.com/"}'
             }

    return {"isBase64Encoded": 'false',
    "statusCode": 200,
    "headers": {},
    "body": '{"url":"http://'+DEST_BUCKET_NAME+'.s3-website-'+S3_LOCATION+'.amazonaws.com/"}'
             }

