from abc import ABC, abstractmethod
from etlops.clients.exceptions import CloudSpecificParameterNotIncluded

class CloudFile:
    _bucket_file_path: str
    _bucket: str
    _cloud_specific_params: dict

    def __init__(self, bucket_file_path: str, bucket: str, cloud_specific_params: dict = None, file_to_upload=None):
        self._bucket_file_path = bucket_file_path
        self._bucket = bucket
        self._cloud_specific_params = cloud_specific_params
        self._file = file_to_upload

    def get_cloud_specific_param(self, parameter: str):
        if parameter not in self._cloud_specific_params.keys():
            raise CloudSpecificParameterNotIncluded(parameter)
        return self._cloud_specific_params[parameter]

    def has_cloud_specific_parameter(self, parameter: str) -> bool:
        return parameter in self._cloud_specific_params.keys()

    def get_bucket_file_path(self) -> str:
        return self._bucket_file_path

    def get_bucket(self) -> str:
        return self._bucket

    def set_file(self, file):
        self._file = file

    def get_file(self):
        return self._file


class CloudStorageClient(ABC):

    BUCKET_ID = "bucket_id"
    BUCKET_CREATED_AT = "created_at"
    OBJECT_KEY = "object_key"
    OBJECT_CREATED_AT = BUCKET_CREATED_AT

    @abstractmethod
    def download(self, cloud_file: CloudFile):
        pass

    @abstractmethod
    def upload(self, cloud_file: CloudFile):
        pass

    @abstractmethod
    def list_buckets(self):
        pass
