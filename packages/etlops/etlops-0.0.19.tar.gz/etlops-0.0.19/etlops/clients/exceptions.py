
class CloudSpecificParameterNotIncluded(Exception):

    def __init__(self, key: str):
        self.missing_parameter = key

    def __str__(self):
        return repr('Parameter {PARAM} not specified in Cloud File.'.format(PARAM=self.missing_parameter))


class CloudStorageOperationModeNotSupported(Exception):

    def __init__(self, selected_operation_type: str, available_operation_modes: tuple):
        self.selected_operation_type = selected_operation_type
        self.available_operation_modes = available_operation_modes

    def __str__(self):
        return repr('GCP blob download type {SELECTED} not provided or not supported, pick one of {OPERATION_TYPES}.'.format(
            OPERATION_TYPES=str(self.available_operation_modes), SELECTED=self.selected_operation_type))


class CloudStorageFileToBeUploadedNotProvided(Exception):

    def __init__(self, bucket_file_path: str, bucket: str):
        self.bucket_file_path = bucket_file_path
        self.bucket = bucket

    def __str__(self):
        return repr('Attempted to upload a file to bucket: {BUCKET} and bucket path: {BUCKET_FILEPATH} without providing the file.'.format(
            BUCKET=self.bucket, BUCKET_FILEPATH=self.bucket_file_path))
