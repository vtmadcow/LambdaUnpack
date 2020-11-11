import unittest
from moto import mock_s3
import boto3
import json
import os
from unpack import unpack

@mock_s3
class TestUnpack(unittest.TestCase):
  DIR_PATH = os.path.dirname(os.path.realpath(__file__))

  SOURCE_BUCKET = "source_bucket"
  DEST_BUCKET = "destination_bucket"
  DEST_KEY = "s3/key/"

  ENV_DEST_KEY = "DEST_KEY"
  ENV_DEST_BUCKET = "DEST_BUCKET"

  def setUp(self):
    os.environ[TestUnpack.ENV_DEST_KEY] = TestUnpack.DEST_KEY
    os.environ[TestUnpack.ENV_DEST_BUCKET] = TestUnpack.DEST_BUCKET

    conn = boto3.resource('s3')
    conn.create_bucket(Bucket=TestUnpack.SOURCE_BUCKET)
    #conn.create_bucket(Bucket=TestUnpack.DEST_BUCKET)

  def tearDown(self):
    #del os.environ[TestUnpack.ENV_DEST_KEY]
    #del os.environ[TestUnpack.ENV_DEST_BUCKET]

    self.remove_bucket(TestUnpack.SOURCE_BUCKET)
    #self.remove_bucket(TestUnpack.DEST_BUCKET)

  @staticmethod
  def remove_bucket(bucket_name):
    s3_bucket = boto3.resource('s3').Bucket(bucket_name)
    s3_bucket.objects.all().delete()
    s3_bucket.delete()

  @staticmethod
  def read_object_bytewise(path):
    return open(path, 'rb')

  @staticmethod
  def put_data_to_s3_object(object_, bucket, s3_source_key):
    boto3.client('s3').put_object(Body=object_, Bucket=bucket, Key=s3_source_key)

  @staticmethod
  def create_s3_event(bucket, key, size):
    return {
      "Records": [
        {
          "s3": {
            "bucket": {
              "name": bucket
            },
            "object": {
              "key": key,
              "size": size
            }
          }
        }
      ]
    }

  def put_file_in_s3(self, input_path, bucket, key):
    with self.read_object_bytewise(input_path) as file_object:
      self.put_data_to_s3_object(file_object, bucket, key)

  def test_extract_tar_successfully(self):
    tar_path = os.path.join(self.DIR_PATH, 'resources', 'unpack_test.tar.gz')
    tar_size = os.path.getsize(tar_path)
    self.put_file_in_s3(tar_path, self.SOURCE_BUCKET, 'unpack_test.tar.gz')

    event = self.create_s3_event(self.SOURCE_BUCKET, 'unpack_test.tar.gz', tar_size)

    unpack_result_message = unpack.unpack_handler(event, None)

    print(unpack_result_message)


if __name__ == '__main__':
    unittest.main()
