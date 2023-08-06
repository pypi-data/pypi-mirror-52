from etlops.clients.awss3 import AWSS3Client, AWSS3Object, CloudStorageClient
from etlops.clients.cloudstorage import CloudFile
from tests.integration.test_assets import constants
from unittest import TestCase, mock, skipIf
from io import BufferedWriter
import os
import string
import random
from datetime import datetime


'''
For the tests to work, these variables need to be filled:
- DOWNLOAD_FILEPATH: AWS S3 key (bucket path) to a file that is present in that bucket
- UPLOAD_FILEPATH: AWS S3 bucket path to a file where the upload is meant to be made
- TEST_BUCKET: Bucket where the operation is meant to be made

Also, make sure the AWS CLI is properly configured in the machine. See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration
'''

DOWNLOAD_FILEPATH = ""
UPLOAD_FILEPATH = "integration_tests/{TEST_NAME}-{FILE_NAME}"
TEST_BUCKET = ""
ENABLE_INTEGRATION_TESTS: bool = bool(os.environ.get(constants.ENABLE_INTEGRATATION_TESTS_KEY))


class TestAWSS3(TestCase):

    def setUp(self) -> None:
        self.aws_client = AWSS3Client()
        self.test_file_content = "{TEST_NAME}-file-content-test"

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_download_file_like_returns_opened_bufferedwritter(self):
        tmp_test_file = TestAWSS3.get_random_string() + ".txt"
        cloud_file = CloudFile(DOWNLOAD_FILEPATH, TEST_BUCKET,
                               dict(aws_download_mode=AWSS3Object.DOWNLOAD_AS_FILE_LIKE,
                                    aws_downloaded_file_path=tmp_test_file))
        downloaded_file: CloudFile = self.aws_client.download(cloud_file)
        self.assertIsInstance(downloaded_file, CloudFile)
        file = downloaded_file.get_file()
        self.assertIsInstance(file, BufferedWriter, msg="Actual type {ACTUAL_TYPE}:".format(ACTUAL_TYPE=type(file)))
        os.remove(tmp_test_file)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_download_as_named_file_returns_bytes(self):
        tmp_test_file = TestAWSS3.get_random_string() + ".txt"
        cloud_file = CloudFile(DOWNLOAD_FILEPATH, TEST_BUCKET,
                               dict(aws_download_mode=AWSS3Object.DOWNLOAD_AS_NAMED_FILE,
                                    aws_downloaded_file_path=tmp_test_file))
        downloaded_file: CloudFile = self.aws_client.download(cloud_file)
        self.assertIsInstance(downloaded_file, CloudFile)
        with open(tmp_test_file, 'rb') as downloaded:
            content = downloaded.read()
            self.assertIsInstance(content, bytes, msg="Actual type {ACTUAL_TYPE}:".format(ACTUAL_TYPE=type(content)))
        os.remove(tmp_test_file)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_upload_as_file_like_properly_uploads_file_from_opened_file(self):
        test_file_content = bytes(
            self.test_file_content.format(TEST_NAME="test_upload_as_file_like_properly_uploads_file_loading_from_file"),
            encoding='utf-8')
        tmp_test_file = TestAWSS3.get_random_string() + ".txt"
        test_bucket_file_path = UPLOAD_FILEPATH.format(FILE_NAME=tmp_test_file,
                                                       TEST_NAME="test_upload_as_file_like_properly_uploads_file_loading_from_file")
        with open(tmp_test_file, 'wb') as file_handle:
            file_handle.write(test_file_content)
        with open(tmp_test_file, 'rb') as file_handle:
            cloud_file = CloudFile(test_bucket_file_path,
                                   TEST_BUCKET,
                                   dict(aws_upload_mode=AWSS3Object.UPLOAD_AS_FILE_LIKE))
            cloud_file.set_file(file_handle)
            self.aws_client.upload(cloud_file)
        cloud_file = CloudFile(test_bucket_file_path,
                               TEST_BUCKET,
                               dict(aws_download_mode=AWSS3Object.DOWNLOAD_AS_NAMED_FILE,
                                    aws_downloaded_file_path=tmp_test_file
                                    ))
        self.aws_client.download(cloud_file)
        with open(tmp_test_file, 'rb') as downloaded_file:
            downloaded_file = AWSS3Object.cast_bytestring(downloaded_file.read())
        self.assertIsInstance(downloaded_file, str, msg='Actual type: ' + str(type(downloaded_file)))
        self.assertEquals(downloaded_file, AWSS3Object.cast_bytestring(test_file_content), msg=downloaded_file)
        os.remove(tmp_test_file)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_upload_as_file_like_properly_uploads_file_from_filepath(self):
        test_file_content = bytes(
            self.test_file_content.format(TEST_NAME="test_upload_as_file_like_properly_uploads_file_loading_from_file"),
            encoding='utf-8')
        tmp_test_file = TestAWSS3.get_random_string() + ".txt"
        test_bucket_file_path = UPLOAD_FILEPATH.format(FILE_NAME=tmp_test_file,
                                                       TEST_NAME="test_upload_as_file_like_properly_uploads_file_loading_from_file")
        with open(tmp_test_file, 'wb') as file_handle:
            file_handle.write(test_file_content)
        cloud_file = CloudFile(test_bucket_file_path,
                               TEST_BUCKET,
                               dict(aws_upload_mode=AWSS3Object.UPLOAD_AS_FILE_LIKE,
                                    aws_uploading_file_path=tmp_test_file))
        self.aws_client.upload(cloud_file)
        cloud_file = CloudFile(test_bucket_file_path,
                               TEST_BUCKET,
                               dict(aws_download_mode=AWSS3Object.DOWNLOAD_AS_NAMED_FILE,
                                    aws_downloaded_file_path=tmp_test_file
                                    ))
        self.aws_client.download(cloud_file)
        with open(tmp_test_file, 'rb') as downloaded_file:
            downloaded_file = AWSS3Object.cast_bytestring(downloaded_file.read())
        self.assertIsInstance(downloaded_file, str, msg='Actual type: ' + str(type(downloaded_file)))
        self.assertEquals(downloaded_file, AWSS3Object.cast_bytestring(test_file_content), msg=downloaded_file)
        os.remove(tmp_test_file)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_upload_as_named_file_properly_uploads_file(self):
        test_file_content = bytes(
            self.test_file_content.format(TEST_NAME="test_upload_as_named_file_properly_uploads_file"),
            encoding='utf-8')
        tmp_test_file = TestAWSS3.get_random_string() + ".txt"
        test_bucket_file_path = UPLOAD_FILEPATH.format(FILE_NAME=tmp_test_file,
                                                       TEST_NAME="test_upload_as_named_file_properly_uploads_file")
        with open(tmp_test_file, 'wb') as file_handle:
            file_handle.write(test_file_content)
        cloud_file = CloudFile(test_bucket_file_path,
                               TEST_BUCKET,
                               dict(aws_upload_mode=AWSS3Object.UPLOAD_AS_NAMED_FILE,
                                    aws_uploading_file_path=tmp_test_file))
        self.aws_client.upload(cloud_file)
        cloud_file = CloudFile(test_bucket_file_path,
                               TEST_BUCKET,
                               dict(aws_download_mode=AWSS3Object.DOWNLOAD_AS_NAMED_FILE,
                                    aws_downloaded_file_path=tmp_test_file))
        self.aws_client.download(cloud_file)
        with open(tmp_test_file, 'rb') as downloaded_file:
            downloaded_file = AWSS3Object.cast_bytestring(downloaded_file.read())
        self.assertIsInstance(downloaded_file, str, msg='Actual type: ' + str(type(downloaded_file)))
        self.assertEquals(downloaded_file, AWSS3Object.cast_bytestring(test_file_content), msg=downloaded_file)
        os.remove(tmp_test_file)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_list_buckets(self):
        for serialized_bucket in self.aws_client.list_buckets():
            self.assertIsInstance(serialized_bucket[CloudStorageClient.BUCKET_ID], str)
            self.assertIsInstance(serialized_bucket[CloudStorageClient.BUCKET_CREATED_AT], datetime)

    @staticmethod
    def get_random_string(size=10):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
