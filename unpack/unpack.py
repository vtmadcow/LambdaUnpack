import urllib.parse
import boto3
import filetype
import io



def unpack_handler(event, context):
  source_bucket = event['Records'][0]['s3']['bucket']['name']
  source_key = urllib.parse.unquote(event['Records'][0]['s3']['object']['key'])

  s3_client = boto3.client('s3')

  s3_object_stream = s3_client.get_object(Bucket=source_bucket, Key=source_key)["Body"]._raw_stream
  
  br = io.BufferedReader(s3_object_stream)
  
  header_bytes = br.peek(261)

  kind = filetype.guess(header_bytes)

  print(kind.mime)

  return {
    "name": "jim"
  }
