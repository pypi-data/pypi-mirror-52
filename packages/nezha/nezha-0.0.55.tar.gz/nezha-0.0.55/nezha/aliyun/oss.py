import os

from oss2 import Auth
from oss2 import Bucket


class OSS(object):
    """
    aliyun oss sdk
    """

    def __init__(self, access_key_id: str, access_key_secret: str, bucket_name: str, endpoint: str):
        self.bucket: Bucket = Bucket(Auth(access_key_id, access_key_secret), endpoint, bucket_name)
        self.get_file_expires: int = 3600 * 24

    def sign_url(self, file_path: str) -> str:
        """
        generate open http url for file in bucket
        :param file_path: 文件的oss存储路径
        """
        return self.bucket.sign_url('GET', file_path, self.get_file_expires)

    @staticmethod
    def generate_file_path(dirpath: str, filename: str) -> str:
        """
        generate upload file_path by filename
        :param filename:
        :return:
        """
        return os.path.join(dirpath, filename)

    def upload(self, file_path: str, file: str) -> bool:
        """
        上传文件到oss
        if picture, file type should be binary.
        :param file_path: 文件的oss存储路径
        :param file: 上传文件
        :return: 上传状态
        """
        result = self.bucket.put_object(key=file_path, data=file)
        return result.status == 200
