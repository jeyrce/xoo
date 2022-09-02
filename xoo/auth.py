from django.contrib.auth.backends import ModelBackend, UserModel


# 因为是单人使用场景，因此实际上无需密码入库
# 自定义登录逻辑, 启动时传递一个环境变量直接作为密码
class AuthBackend(ModelBackend):
    """
    通过用户名、邮箱、电话都可以登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
