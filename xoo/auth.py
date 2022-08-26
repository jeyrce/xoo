from django.contrib.auth.backends import ModelBackend, UserModel

from xoo.settings import AUTH_USERNAME, AUTH_PASSWORD


# 因为是单人使用场景，因此实际上无需密码入库
# 自定义登录逻辑, 启动时传递一个环境变量直接作为密码
class AuthBackend(ModelBackend):
    """
    仅使用一个超级用户，且不管输入的用户名，只校验口令
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            account = UserModel.objects.get(**{UserModel.USERNAME_FIELD: AUTH_USERNAME})
        except UserModel.DoesNotExist:
            return None
        else:
            if password == AUTH_PASSWORD:
                return account
        return None
