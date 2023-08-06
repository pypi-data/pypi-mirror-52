from etlops.clients.cloudstorage import CloudFile
from etlops.clients.gcpstorage import GCPStorageClient, GCPStorageBlob, storage, CloudStorageClient
from tests.integration.test_assets import constants
from unittest import TestCase, mock, skipIf
from io import BufferedWriter
import os
from datetime import datetime
import string
import random

'''
For the tests to work, these variables need to be filled:
- ENVIRONMENT_CREDENTIALS: GOOGLE_APPLICATION_CREDENTIALS in an absolute or relative path to a GCP service account credential
json
- DOWNLOAD_FILEPATH: GCP Storage bucket path to a file that is present in that bucket
- UPLOAD_FILEPATH: GCP Storage bucket path to a file where the upload is meant to be made
'''
ENVIRONMENT_CREDENTIALS = {
    constants.GOOGLE_APPLICATION_CREDENTIALS: ""}
DOWNLOAD_FILEPATH = ""
UPLOAD_FILEPATH = "integration_tests/{TEST_NAME}-{FILE_NAME}"
TEST_BUCKET = ""
ENABLE_INTEGRATION_TESTS: bool = bool(os.environ.get(constants.ENABLE_INTEGRATATION_TESTS_KEY))


class TestGCPStorage(TestCase):

    @mock.patch.dict('os.environ', ENVIRONMENT_CREDENTIALS)
    def setUp(self) -> None:
        self.gcp_client = GCPStorageClient()
        self.test_file_content = "{TEST_NAME}-file-content-test"

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_download_string_returns_bytestring(self):
        cloud_file = CloudFile(DOWNLOAD_FILEPATH, TEST_BUCKET,
                               dict(gcp_download_mode=GCPStorageBlob.DOWNLOAD_AS_STRING))
        downloaded_file: CloudFile = self.gcp_client.download(cloud_file)
        self.assertIsInstance(downloaded_file.get_file(), bytes)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_download_string_returns_bytestring_thats_convertible_into_string(self):
        cloud_file = CloudFile(DOWNLOAD_FILEPATH, TEST_BUCKET,
                               dict(gcp_download_mode=GCPStorageBlob.DOWNLOAD_AS_STRING))
        downloaded_file: CloudFile = self.gcp_client.download(cloud_file)
        parsed_downloaded_file: str = GCPStorageBlob.cast_bytestring(downloaded_file.get_file())
        self.assertIsInstance(parsed_downloaded_file, str)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_download_file_like_returns_opened_bufferedwritter(self):
        tmp_test_file = TestGCPStorage.get_random_string() + ".txt"
        cloud_file = CloudFile(DOWNLOAD_FILEPATH, TEST_BUCKET,
                               dict(gcp_download_mode=GCPStorageBlob.DOWNLOAD_AS_FILE_LIKE,
                                    gcp_downloaded_file_path=tmp_test_file))
        downloaded_file: CloudFile = self.gcp_client.download(cloud_file)
        self.assertIsInstance(downloaded_file, CloudFile)
        file = downloaded_file.get_file()
        self.assertIsInstance(file, BufferedWriter, msg="Actual type {ACTUAL_TYPE}:".format(ACTUAL_TYPE=type(file)))
        os.remove(tmp_test_file)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_download_as_named_file_returns_bytes(self):
        tmp_test_file = TestGCPStorage.get_random_string() + ".txt"
        cloud_file = CloudFile(DOWNLOAD_FILEPATH, TEST_BUCKET,
                               dict(gcp_download_mode=GCPStorageBlob.DOWNLOAD_AS_NAMED_FILE,
                                    gcp_downloaded_file_path=tmp_test_file))
        downloaded_file: CloudFile = self.gcp_client.download(cloud_file)
        self.assertIsInstance(downloaded_file, CloudFile)
        with open(tmp_test_file, 'rb') as downloaded:
            content = downloaded.read()
            self.assertIsInstance(content, bytes, msg="Actual type {ACTUAL_TYPE}:".format(ACTUAL_TYPE=type(content)))
        os.remove(tmp_test_file)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_upload_string_properly_uploads_file(self):
        tmp_test_file = TestGCPStorage.get_random_string() + ".txt"
        test_file_content = self.test_file_content.format(TEST_NAME="test_upload_string_properly_uploads_file")
        test_bucket_file_path = UPLOAD_FILEPATH.format(FILE_NAME=tmp_test_file,
                                                       TEST_NAME="test_upload_string_properly_uploads_file")
        cloud_file = CloudFile(test_bucket_file_path,
                               TEST_BUCKET,
                               dict(gcp_upload_mode=GCPStorageBlob.UPLOAD_AS_STRING),
                               test_file_content)
        self.gcp_client.upload(cloud_file)
        cloud_file = CloudFile(test_bucket_file_path,
                               TEST_BUCKET,
                               dict(gcp_download_mode=GCPStorageBlob.DOWNLOAD_AS_STRING))
        downloaded_file: CloudFile = self.gcp_client.download(cloud_file)
        parsed_downloaded_file: str = GCPStorageBlob.cast_bytestring(downloaded_file.get_file())
        self.assertIsInstance(parsed_downloaded_file, str, msg='Actual type: ' + str(type(parsed_downloaded_file)))
        self.assertEquals(parsed_downloaded_file, test_file_content, msg=parsed_downloaded_file)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_upload_as_file_like_properly_uploads_file_from_opened_file(self):
        test_file_content = bytes(
            self.test_file_content.format(TEST_NAME="test_upload_as_file_like_properly_uploads_file_from_opened_file"),
            encoding='utf-8')
        tmp_test_file = TestGCPStorage.get_random_string() + ".txt"
        test_bucket_file_path = UPLOAD_FILEPATH.format(FILE_NAME=tmp_test_file,
                                                       TEST_NAME="test_upload_as_file_like_properly_uploads_file_from_opened_file")
        with open(tmp_test_file, 'wb') as file_handle:
            file_handle.write(test_file_content)
        with open(tmp_test_file, 'rb') as file_handle:
            cloud_file = CloudFile(test_bucket_file_path,
                                   TEST_BUCKET,
                                   dict(gcp_upload_mode=GCPStorageBlob.UPLOAD_AS_FILE_LIKE))
            cloud_file.set_file(file_handle)
            self.gcp_client.upload(cloud_file)
        cloud_file = CloudFile(test_bucket_file_path,
                               TEST_BUCKET,
                               dict(gcp_download_mode=GCPStorageBlob.DOWNLOAD_AS_STRING))
        downloaded_file = GCPStorageBlob.cast_bytestring(self.gcp_client.download(cloud_file).get_file())
        self.assertIsInstance(downloaded_file, str, msg='Actual type: ' + str(type(downloaded_file)))
        self.assertEquals(downloaded_file, GCPStorageBlob.cast_bytestring(test_file_content), msg=downloaded_file)
        os.remove(tmp_test_file)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_upload_as_file_like_properly_uploads_file_from_filepath(self):
        test_file_content = bytes(
            self.test_file_content.format(TEST_NAME="test_upload_as_file_like_properly_uploads_file_from_filepath"),
            encoding='utf-8')
        tmp_test_file = TestGCPStorage.get_random_string() + ".txt"
        test_bucket_file_path = UPLOAD_FILEPATH.format(FILE_NAME=tmp_test_file,
                                                       TEST_NAME="test_upload_as_file_like_properly_uploads_file_from_filepath")
        with open(tmp_test_file, 'wb') as file_handle:
            file_handle.write(test_file_content)
        cloud_file = CloudFile(test_bucket_file_path,
                               TEST_BUCKET,
                               dict(gcp_upload_mode=GCPStorageBlob.UPLOAD_AS_FILE_LIKE,
                                    gcp_uploading_file_path=tmp_test_file))
        self.gcp_client.upload(cloud_file)
        cloud_file = CloudFile(test_bucket_file_path,
                               TEST_BUCKET,
                               dict(gcp_download_mode=GCPStorageBlob.DOWNLOAD_AS_STRING))
        downloaded_file = GCPStorageBlob.cast_bytestring(self.gcp_client.download(cloud_file).get_file())
        self.assertIsInstance(downloaded_file, str, msg='Actual type: ' + str(type(downloaded_file)))
        self.assertEquals(downloaded_file, GCPStorageBlob.cast_bytestring(test_file_content), msg=downloaded_file)
        os.remove(tmp_test_file)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_upload_as_named_file_properly_uploads_file(self):
        test_file_content = bytes(
            self.test_file_content.format(TEST_NAME="test_upload_as_named_file_properly_uploads_file"),
            encoding='utf-8')
        tmp_test_file = TestGCPStorage.get_random_string() + ".txt"
        test_bucket_file_path = UPLOAD_FILEPATH.format(FILE_NAME=tmp_test_file,
                                                       TEST_NAME="test_upload_as_named_file_properly_uploads_file")
        with open(tmp_test_file, 'wb') as file_handle:
            file_handle.write(test_file_content)
        cloud_file = CloudFile(test_bucket_file_path,
                               TEST_BUCKET,
                               dict(gcp_upload_mode=GCPStorageBlob.UPLOAD_AS_NAMED_FILE,
                                    gcp_uploading_file_path=tmp_test_file))
        self.gcp_client.upload(cloud_file)
        cloud_file = CloudFile(test_bucket_file_path,
                               TEST_BUCKET,
                               dict(gcp_download_mode=GCPStorageBlob.DOWNLOAD_AS_STRING))
        downloaded_file = GCPStorageBlob.cast_bytestring(self.gcp_client.download(cloud_file).get_file())
        self.assertIsInstance(downloaded_file, str, msg='Actual type: ' + str(type(downloaded_file)))
        self.assertEquals(downloaded_file, GCPStorageBlob.cast_bytestring(test_file_content), msg=downloaded_file)
        os.remove(tmp_test_file)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_list_buckets(self):
        for serialized_bucket in self.gcp_client.list_buckets():
            self.assertIsInstance(serialized_bucket[CloudStorageClient.BUCKET_ID], str)
            self.assertIsInstance(serialized_bucket[CloudStorageClient.BUCKET_CREATED_AT], datetime)

    @skipIf(ENABLE_INTEGRATION_TESTS, 'Skipping integration tests')
    def test_get_bucket(self):
        for serialized_bucket in self.gcp_client.list_buckets():
            bucket = self.gcp_client.get_bucket(bucket_id=serialized_bucket[CloudStorageClient.BUCKET_ID])
            self.assertIsInstance(bucket, storage.bucket.Bucket)

    @staticmethod
    def get_random_string(size=10):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
