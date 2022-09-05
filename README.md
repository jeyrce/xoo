# xoo

私人账本: http://xoo.site

- 前台展示直接使用腾讯兔小巢: [https://txc.qq.com/](https://txc.qq.com/)
- 后台使用 [django-admin](https://docs.djangoproject.com/en/4.1/intro/tutorial07/)
  + [simpleui](https://simpleui.72wo.com/docs/simpleui/doc.html) 快速创建内容管理系统
- 整合七牛云kodo对象存储作为 media 后端

```shell
mkvirtualenv xoo

pip install -r requirements.txt

python manage.py makemigrations xoo

python manage.py migrate

python manage.py createsuperuser
```
