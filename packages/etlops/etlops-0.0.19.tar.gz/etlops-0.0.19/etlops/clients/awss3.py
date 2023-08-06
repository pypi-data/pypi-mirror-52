import boto3
from etlops.clients.cloudstorage import CloudStorageClient, CloudFile
from etlops.clients.exceptions import CloudSpecificParameterNotIncluded, CloudStorageOperationModeNotSupported, \
    CloudStorageFileToBeUploadedNotProvided


class AWSS3Object:
    DOWNLOAD_AS_NAMED_FILE = 'named_file'
    DOWNLOAD_AS_FILE_LIKE = 'file-like'

    AWS_SP_DOWNLOAD_MODE = "aws_download_mode"
    AWS_SP_DOWNLOAD_FILEPATH = "aws_bucket_filepath"
    AWS_SP_UPLOAD_MODE = "aws_upload_mode"
    AWS_SP_UPLOAD_FILEPATH = AWS_SP_DOWNLOAD_FILEPATH
    AWS_SP_DOWNLOADED_FILE_PATH = "aws_downloaded_file_path"
    AWS_SP_UPLOADING_FILE_PATH = "aws_uploading_file_path"

    AWS_AVAILABLE_DOWNLOAD_MODES = (DOWNLOAD_AS_NAMED_FILE,
                                    DOWNLOAD_AS_FILE_LIKE)  # see download_* methods at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object

    UPLOAD_AS_NAMED_FILE = DOWNLOAD_AS_NAMED_FILE
    UPLOAD_AS_FILE_LIKE = DOWNLOAD_AS_FILE_LIKE

    AWS_AVAILABLE_UPLOAD_MODES = (UPLOAD_AS_NAMED_FILE,
                                  UPLOAD_AS_FILE_LIKE)  # see upload_* methods at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object

    DOWNLOAD_OPERATION = 'DOWNLOAD'
    UPLOAD_OPERATION = 'UPLOAD'
    OPERATION_AVAILABLE_MODES = 'AVAILABLE_MODES'
    OPERATION_MODE_KEY = "MODE_KEY"
    OPERATION_CONSTANTS = {
        DOWNLOAD_OPERATION: {
            OPERATION_MODE_KEY: AWS_SP_DOWNLOAD_MODE,
            OPERATION_AVAILABLE_MODES: AWS_AVAILABLE_DOWNLOAD_MODES
        },
        UPLOAD_OPERATION: {
            OPERATION_MODE_KEY: AWS_SP_UPLOAD_MODE,
            OPERATION_AVAILABLE_MODES: AWS_AVAILABLE_UPLOAD_MODES
        },
    }

    def __init__(self, obj):
        self._obj = obj

    def download(self, cloud_file: CloudFile) -> CloudFile:
        download_mode = self._get_operation_mode(cloud_file=cloud_file,
                                                 operation_kind=AWSS3Object.DOWNLOAD_OPERATION)
        if download_mode == AWSS3Object.DOWNLOAD_AS_FILE_LIKE:
            downloaded_cloud_file = self.__download_as_file_like(cloud_file)
        else:
            downloaded_cloud_file = self.__download_as_named_file(cloud_file)
        return downloaded_cloud_file

    def __download_as_file_like(self, cloud_file: CloudFile) -> CloudFile:
        local_file_path = self._fetch_specific_parameter(cloud_file, AWSS3Object.AWS_SP_DOWNLOADED_FILE_PATH)
        with open(local_file_path, 'wb') as file:
            self._obj.download_fileobj(Fileobj=file)
            cloud_file.set_file(file)
        return cloud_file

    def __download_as_named_file(self, cloud_file: CloudFile) -> CloudFile:
        local_file_path = self._fetch_specific_parameter(cloud_file, AWSS3Object.AWS_SP_DOWNLOADED_FILE_PATH)
        with open(local_file_path, 'wb'):
            self._obj.download_file(Filename=local_file_path)
        return cloud_file

    def upload(self, cloud_file: CloudFile) -> None:
        upload_mode = self._get_operation_mode(cloud_file=cloud_file,
                                               operation_kind=AWSS3Object.UPLOAD_OPERATION)
        if upload_mode == AWSS3Object.UPLOAD_AS_FILE_LIKE:
            self.__upload_as_file_like(cloud_file)
        else:
            self.__upload_as_named_file(cloud_file)

    def __upload_as_file_like(self, cloud_file: CloudFile) -> None:
        if cloud_file.has_cloud_specific_parameter(AWSS3Object.AWS_SP_UPLOADING_FILE_PATH):
            file_path = self._fetch_specific_parameter(cloud_file, AWSS3Object.AWS_SP_UPLOADING_FILE_PATH)
            with open(file_path, 'rb') as file:
                self._obj.upload_fileobj(Fileobj=file)
        else:
            self._validate_file_to_be_uploaded(cloud_file)
            self._obj.upload_fileobj(Fileobj=cloud_file.get_file())

    def __upload_as_named_file(self, cloud_file: CloudFile) -> None:
        file_path = self._fetch_specific_parameter(cloud_file, AWSS3Object.AWS_SP_UPLOADING_FILE_PATH)
        self._obj.upload_file(Filename=file_path)
        return None

    @staticmethod
    def cast_bytestring(byte_string: bytes, encoding: str = 'utf-8') -> str:
        return str(byte_string, encoding=encoding)

    def _get_operation_mode(self, cloud_file: CloudFile, operation_kind: str) -> str:
        operation_constants = AWSS3Object.OPERATION_CONSTANTS[operation_kind]
        operation_mode_parameter_key = operation_constants[AWSS3Object.OPERATION_MODE_KEY]
        operation_mode = self._fetch_specific_parameter(cloud_file, operation_mode_parameter_key)
        if operation_mode not in operation_constants[AWSS3Object.OPERATION_AVAILABLE_MODES]:
            raise CloudStorageOperationModeNotSupported(operation_mode,
                                                        operation_constants[AWSS3Object.OPERATION_AVAILABLE_MODES])
        return operation_mode

    def _fetch_specific_parameter(self, cloud_file: CloudFile, key: str):
        if not cloud_file.has_cloud_specific_parameter(key):
            raise CloudSpecificParameterNotIncluded(key)
        return cloud_file.get_cloud_specific_param(key)

    def _validate_file_to_be_uploaded(self, cloud_file: CloudFile) -> None:
        file_to_upload = cloud_file.get_file()
        if file_to_upload is None:
            raise CloudStorageFileToBeUploadedNotProvided(cloud_file.get_bucket_file_path(), cloud_file.get_bucket())


class AWSS3Client(CloudStorageClient):
    BUCKETS_KEY = 'Buckets'
    BUCKET_NAME = 'Name'
    BUCKET_CREATION_DATE = 'CreationDate'
    AWS_S3_RESOURCE_ID = 's3'

    def __init__(self):
        self._s3resource = boto3.resource(AWSS3Client.AWS_S3_RESOURCE_ID)
        self._client = boto3.client(AWSS3Client.AWS_S3_RESOURCE_ID)

    def download(self, cloud_file: CloudFile):
        obj = self.build_object(cloud_file.get_bucket_file_path(), cloud_file.get_bucket())
        wrapped_object = AWSS3Object(obj)
        return wrapped_object.download(cloud_file)

    def upload(self, cloud_file: CloudFile):
        obj = self.build_object(cloud_file.get_bucket_file_path(), cloud_file.get_bucket())
        wrapped_object = AWSS3Object(obj)
        return wrapped_object.upload(cloud_file)

    def list_buckets(self) -> list:
        standardized_buckets = []
        buckets_object = self._client.list_buckets()
        for bucket in buckets_object[AWSS3Client.BUCKETS_KEY]:
            standardized_buckets.append({CloudStorageClient.BUCKET_ID: bucket[AWSS3Client.BUCKET_NAME],
                                         CloudStorageClient.BUCKET_CREATED_AT: bucket[AWSS3Client.BUCKET_CREATION_DATE]})
        return standardized_buckets

    def get_bucket(self, bucket_id: str):
        return self._s3resource.Bucket(name=bucket_id)

    def list_bucket_objects(self, bucket_id: str) -> list:
        object_list = list()
        bucket = self.get_bucket(bucket_id)
        for obj in bucket.objects.all():
            object_list.append({
                CloudStorageClient.OBJECT_KEY: obj.key,
                CloudStorageClient.BUCKET_ID: obj.bucket_name,
                CloudStorageClient.OBJECT_CREATED_AT: obj.last_modified
            })
        return object_list

    def build_object(self, bucket_file_path: str, bucket_name: str):
        return self._s3resource.Object(bucket_name=bucket_name, key=bucket_file_path)
