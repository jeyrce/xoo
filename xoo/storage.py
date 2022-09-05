import http.client
import os.path

from django.core.files.storage import Storage
from django.conf import settings

import qiniu


# 七牛云对象存储, 只需实现关键的上传和删除即可，其他方法均无须实现
class QiNiuStorage(Storage):

    def __init__(self):
        self.qiniu_ak = settings.QINIU_AK
        self.qiniu_sk = settings.QINIU_SK
        self.qiniu_bucket = settings.QINIU_BUCKET
        self.qiniu_base_url = settings.QINIU_BASE_URL

    def _open(self, name, mode='rb'):
        """
            无需打开文件，忽略
        """
        pass

    # 上传至七牛云保存
    def _save(self, name, content):
        token = qiniu.Auth(self.qiniu_ak, self.qiniu_sk).upload_token(self.qiniu_bucket)
        res, info = qiniu.put_data(
            up_token=token,
            key=name,
            data=content.file if isinstance(content.file, bytes) else content.file.read(),
        )
        if info.status_code == http.HTTPStatus.OK:
            return res.get('key')
        raise Exception('上传七牛云失败: {}'.format(info.text_body))

    def path(self, name):
        """
        https://docs.djangoproject.com/en/4.1/howto/custom-file-storage/
        不提供本地存储，因此无须实现该方法
        """
        pass

    def delete(self, name):
        bucket = qiniu.BucketManager(qiniu.Auth(self.qiniu_ak, self.qiniu_sk), settings.QINIU_BUCKET)
        res, info = bucket.delete_after_days(self.qiniu_bucket, name, settings.QINIU_DELETE_AFTER_DAYS)
        if info.status_code == http.HTTPStatus.OK:
            return True
        raise Exception('七牛云删除失败: {}'.format(res))

    def exists(self, name):
        """
        1、通过七牛云开启覆盖上传模式
        2、七牛云自动返回存在判断
        综上，此处逻辑不做处理
        """
        return False

    def listdir(self, path):
        """
        对象存储无须实现该方法，此处默认返回空列表
        """
        return [], []

    def size(self, name):
        pass

    def url(self, name):
        """
        文件的完整存储路径
        :param name: db中保存的路径
        :return:
        """
        return os.path.join(self.qiniu_base_url, name)

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

    def get_modified_time(self, name):
        pass
