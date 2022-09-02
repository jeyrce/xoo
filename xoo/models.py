import string

import shortuuid
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth import get_user_model

from xoo import aes

UserModel = get_user_model()
normal_uuid = shortuuid.ShortUUID(string.digits + string.ascii_lowercase)
order_uuid = shortuuid.ShortUUID(string.digits)
uuid_length = 12
order_length = 9


class MetaModel(models.Model):
    uuid = models.CharField(max_length=uuid_length, primary_key=True, default=normal_uuid.uuid(pad_length=uuid_length))
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='最后更新', auto_now=True, null=True)
    deleted_at = models.DateTimeField(verbose_name='删除时间', null=True)

    objects = models.Manager()


# 自定义加密字符字段, 加密存库, 解密输出(只在后台管理系统可以看到明文)
class SecureField(models.CharField):
    def __init__(self, *args, db_collation=None, **kwargs):
        self.max_length = 64
        super().__init__(*args, db_collation, **kwargs)

    # 入库保存前进行aes加密
    # 限定长度为64, 因此超过31字符则证明已经加密过
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if add or len(value) < (self.max_length / 2):
            setattr(model_instance, self.attname, aes.encrypt(value))
        super().pre_save(model_instance, add)


# 建档立卡: 客户资料, 用于后期进行合作挖掘
class Account(MetaModel, models.Model):
    username = models.CharField(max_length=32, unique=True, verbose_name='客户称呼', null=False, blank=False)
    mobile = models.CharField(max_length=128, unique=True, verbose_name='手机', null=True, blank=True)  # 需要脱敏保存
    email = models.EmailField(verbose_name='邮箱', blank=True, null=True)
    wechat = models.CharField(verbose_name='微信', max_length=64, null=True, blank=True)
    qq = models.CharField(verbose_name='QQ', max_length=12, null=True, blank=True)
    git = models.URLField(verbose_name='git账户', null=True, blank=True)
    IdCard = models.CharField(verbose_name='身份证', null=True, blank=True, max_length=18)  # 需要脱敏保存
    annotation = models.TextField(verbose_name='备注', null=True, blank=True)
    source = models.CharField(verbose_name='客户来源', max_length=64, null=True, blank=True)

    class Meta:
        verbose_name_plural = verbose_name = '客户资料'
        db_table = 'account'

    def __str__(self):
        return self.username

    # 客户订单总额
    def amount(self):
        sum = 0
        Ticket.objects.filter()


# 文件清单：关联需求文件等
class File(MetaModel, models.Model):
    project = models.ForeignKey(to='Project', related_name='files', on_delete=models.CASCADE, verbose_name='所属项目',
                                null=True, blank=True)
    filename = models.FileField(upload_to='uploads/', null=True, blank=True, verbose_name='文件链接')

    class Meta:
        verbose_name_plural = verbose_name = '文件附件'
        db_table = 'file'

    def __str__(self):
        return self.filename


# 项目任务
class Project(MetaModel, models.Model):
    name = models.CharField(verbose_name='项目名称', max_length=128)
    owner = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name='开发者')
    account = models.ForeignKey(to=Account, on_delete=models.CASCADE, null=True, blank=True, verbose_name='客户')
    detail = RichTextField(verbose_name='详情', blank=True, null=True)
    mobile = models.CharField(max_length=11, verbose_name='联系电话', blank=True, null=True, unique=True)
    contact = models.CharField(max_length=32, verbose_name='联系人', blank=True, null=True)
    email = models.EmailField(verbose_name='联系邮箱', blank=True, null=True)
    wechat = models.CharField(verbose_name='微信号', max_length=32, blank=True, null=True)
    days = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='工时(天)')
    image_hub = models.URLField(verbose_name='镜像仓库', blank=True, null=True)
    code_hub = models.URLField(verbose_name='代码仓库', blank=True, null=True)
    online_url = models.URLField(verbose_name='线上地址', blank=True, null=True)
    finished = models.BooleanField(default=False, verbose_name='是否已完成')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='标定价格', default=0)

    class Meta:
        verbose_name_plural = verbose_name = '项目信息'
        db_table = 'project'

    def __str__(self):
        return self.name

    # 实际收益金额
    def amount(self):
        summary = 0
        tickets = Ticket.objects.filter(project_id=self.pk).all()
        for ticket in tickets:
            if ticket.number > 0:
                summary += ticket.number
        return summary


# 收款记录(账本): 支付宝红包口令即9位uuid
class Ticket(MetaModel, models.Model):
    uuid = models.CharField(max_length=order_length, primary_key=True, default=order_uuid.uuid(pad_length=order_length))
    project = models.ForeignKey(to=Project, related_name='tickets', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='所属项目')
    account = models.ForeignKey(to=Account, related_name='tickets', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='客户')
    number = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='金额', default=0)
    annotation = models.CharField(max_length=64, verbose_name='备注', null=True, blank=True)
    validated_at = models.DateTimeField(verbose_name='核销时间', null=True)
