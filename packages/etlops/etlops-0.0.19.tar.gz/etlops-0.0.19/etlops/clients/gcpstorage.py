from google.cloud import storage
from etlops.clients.cloudstorage import CloudFile, CloudStorageClient
from etlops.clients.exceptions import CloudSpecificParameterNotIncluded, CloudStorageOperationModeNotSupported, \
    CloudStorageFileToBeUploadedNotProvided


class GCPStorageBlob:
    DOWNLOAD_AS_STRING = 'string'
    DOWNLOAD_AS_NAMED_FILE = 'named_file'
    DOWNLOAD_AS_FILE_LIKE = 'file-like'

    GCP_SP_DOWNLOAD_MODE = "gcp_download_mode"
    GCP_SP_DOWNLOAD_FILEPATH = "gcp_bucket_filepath"
    GCP_SP_UPLOAD_MODE = "gcp_upload_mode"
    GCP_SP_UPLOAD_FILEPATH = GCP_SP_DOWNLOAD_FILEPATH
    GCP_SP_DOWNLOADED_FILE_PATH = "gcp_downloaded_file_path"
    GCP_SP_UPLOADING_FILE_PATH = "gcp_uploading_file_path"

    GCP_AVAILABLE_DOWNLOAD_MODES = (DOWNLOAD_AS_STRING, DOWNLOAD_AS_NAMED_FILE,
                                    DOWNLOAD_AS_FILE_LIKE)  # see download_* methods at https://googleapis.github.io/google-cloud-python/latest/storage/blobs.html

    UPLOAD_AS_STRING = DOWNLOAD_AS_STRING
    UPLOAD_AS_NAMED_FILE = DOWNLOAD_AS_NAMED_FILE
    UPLOAD_AS_FILE_LIKE = DOWNLOAD_AS_FILE_LIKE

    GCP_DEFAULT_UPLOAD_MODE = UPLOAD_AS_STRING
    GCP_AVAILABLE_UPLOAD_MODES = (UPLOAD_AS_STRING, UPLOAD_AS_NAMED_FILE,
                                  UPLOAD_AS_FILE_LIKE)  # see upload_* methods at https://googleapis.github.io/google-cloud-python/latest/storage/blobs.html

    DOWNLOAD_OPERATION = 'DOWNLOAD'
    UPLOAD_OPERATION = 'UPLOAD'
    OPERATION_AVAILABLE_MODES = 'AVAILABLE_MODES'
    OPERATION_MODE_KEY = "MODE_KEY"
    OPERATION_CONSTANTS = {
        DOWNLOAD_OPERATION: {
            OPERATION_MODE_KEY: GCP_SP_DOWNLOAD_MODE,
            OPERATION_AVAILABLE_MODES: GCP_AVAILABLE_DOWNLOAD_MODES
        },
        UPLOAD_OPERATION: {
            OPERATION_MODE_KEY: GCP_SP_UPLOAD_MODE,
            OPERATION_AVAILABLE_MODES: GCP_AVAILABLE_UPLOAD_MODES
        }
    }
    _blob: storage.Blob

    def __init__(self, blob: storage.Blob):
        self._blob = blob

    def download(self, cloud_file: CloudFile) -> CloudFile:
        download_mode = self._get_operation_mode(cloud_file=cloud_file,
                                                 operation_kind=GCPStorageBlob.DOWNLOAD_OPERATION)
        if download_mode == GCPStorageBlob.DOWNLOAD_AS_FILE_LIKE:
            downloaded_cloud_file = self.__download_as_file_like(cloud_file)
        elif download_mode == GCPStorageBlob.DOWNLOAD_AS_NAMED_FILE:
            downloaded_cloud_file = self.__download_as_named_file(cloud_file)
        else:
            downloaded_cloud_file = self.__download_as_string(cloud_file)
        return downloaded_cloud_file

    def __download_as_string(self, cloud_file: CloudFile) -> CloudFile:
        cloud_file.set_file(self._blob.download_as_string())
        return cloud_file

    def __download_as_file_like(self, cloud_file: CloudFile) -> CloudFile:
        local_file_path = self._fetch_specific_parameter(cloud_file, GCPStorageBlob.GCP_SP_DOWNLOADED_FILE_PATH)
        with open(local_file_path, 'wb') as file:
            self._blob.download_to_file(file)
            cloud_file.set_file(file)
        return cloud_file

    def __download_as_named_file(self, cloud_file: CloudFile) -> CloudFile:
        local_file_path = self._fetch_specific_parameter(cloud_file, GCPStorageBlob.GCP_SP_DOWNLOADED_FILE_PATH)
        with open(local_file_path, 'wb'):
            self._blob.download_to_filename(filename=local_file_path)
        return cloud_file

    def upload(self, cloud_file: CloudFile) -> None:
        upload_mode = self._get_operation_mode(cloud_file=cloud_file,
                                               operation_kind=GCPStorageBlob.UPLOAD_OPERATION)
        if upload_mode == GCPStorageBlob.UPLOAD_AS_FILE_LIKE:
            self.__upload_as_file_like(cloud_file)
        elif upload_mode == GCPStorageBlob.UPLOAD_AS_NAMED_FILE:
            self.__upload_as_named_file(cloud_file)
        else:
            self.__upload_as_string(cloud_file)

    def __upload_as_string(self, cloud_file: CloudFile) -> None:
        self._validate_file_to_be_uploaded(cloud_file)
        self._blob.upload_from_string(cloud_file.get_file())

    def __upload_as_file_like(self, cloud_file: CloudFile) -> None:
        if cloud_file.has_cloud_specific_parameter(GCPStorageBlob.GCP_SP_UPLOADING_FILE_PATH):
            file_path = self._fetch_specific_parameter(cloud_file, GCPStorageBlob.GCP_SP_UPLOADING_FILE_PATH)
            with open(file_path, 'rb') as file:
                self._blob.upload_from_file(file_obj=file)
        else:
            self._validate_file_to_be_uploaded(cloud_file)
            self._blob.upload_from_file(file_obj=cloud_file.get_file())

    def __upload_as_named_file(self, cloud_file: CloudFile) -> None:
        file_path = self._fetch_specific_parameter(cloud_file, GCPStorageBlob.GCP_SP_UPLOADING_FILE_PATH)
        self._blob.upload_from_filename(filename=file_path)
        return None

    def _validate_file_to_be_uploaded(self, cloud_file: CloudFile) -> None:
        file_to_upload = cloud_file.get_file()
        if file_to_upload is None:
            raise CloudStorageFileToBeUploadedNotProvided(cloud_file.get_bucket_file_path(), cloud_file.get_bucket())

    @staticmethod
    def cast_bytestring(byte_string: bytes, encoding: str = 'utf-8') -> str:
        return str(byte_string, encoding=encoding)

    def _get_operation_mode(self, cloud_file: CloudFile, operation_kind: str) -> str:
        operation_constants = GCPStorageBlob.OPERATION_CONSTANTS[operation_kind]
        operation_mode_parameter_key = operation_constants[GCPStorageBlob.OPERATION_MODE_KEY]
        operation_mode = self._fetch_specific_parameter(cloud_file, operation_mode_parameter_key)
        if operation_mode not in operation_constants[GCPStorageBlob.OPERATION_AVAILABLE_MODES]:
            raise CloudStorageOperationModeNotSupported(operation_mode,
                                                        operation_constants[GCPStorageBlob.OPERATION_AVAILABLE_MODES])
        return operation_mode

    def _fetch_specific_parameter(self, cloud_file: CloudFile, key: str):
        if not cloud_file.has_cloud_specific_parameter(key):
            raise CloudSpecificParameterNotIncluded(key)
        return cloud_file.get_cloud_specific_param(key)


class GCPStorageClient(CloudStorageClient):

    _client: storage.Client

    def __init__(self):
        self._client = storage.Client()

    def download(self, cloud_file: CloudFile) -> CloudFile:
        blob: storage.Blob = self.build_object(cloud_file.get_bucket_file_path(), cloud_file.get_bucket())
        wrapped_blob: GCPStorageBlob = GCPStorageBlob(blob)
        return wrapped_blob.download(cloud_file)

    def upload(self, cloud_file: CloudFile) -> None:
        blob: storage.Blob = self.build_object(cloud_file.get_bucket_file_path(), cloud_file.get_bucket())
        wrapped_blob: GCPStorageBlob = GCPStorageBlob(blob)
        wrapped_blob.upload(cloud_file)

    def list_buckets(self) -> list:
        bucket_list = list()
        for bucket in self._client.list_buckets():
            bucket_list.append({CloudStorageClient.BUCKET_CREATED_AT: bucket.time_created,
                                CloudStorageClient.BUCKET_ID: bucket.id})
        return bucket_list

    def get_bucket(self, bucket_id: str) -> storage.bucket.Bucket:
        return self._client.get_bucket(bucket_or_name=bucket_id)

    def list_bucket_objects(self, bucket_id: str) -> list:
        object_list = list()
        bucket = self.get_bucket(bucket_id)
        for obj in bucket.list_blobs():
            object_list.append({
                CloudStorageClient.OBJECT_KEY: obj.name,
                CloudStorageClient.BUCKET_ID: bucket_id,
                CloudStorageClient.OBJECT_CREATED_AT: obj.time_created
            })
        return object_list

    def build_object(self, bucket_file_path: str, bucket_name: str) -> storage.Blob:
        bucket: storage.Bucket = self._client.get_bucket(bucket_or_name=bucket_name)
        return bucket.blob(bucket_file_path)
