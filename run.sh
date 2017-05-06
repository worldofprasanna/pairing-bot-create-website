rm Archive.zip
zip -r Archive.zip *
aws lambda update-function-code --function-name spark-create-blog --zip-file fileb://Archive.zip
