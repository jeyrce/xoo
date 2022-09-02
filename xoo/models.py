import string

import shortuuid
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth import get_user_model

from xoo import aes

UserModel = get_user_model()
normal_uuid = shortuuid.ShortUUID(string.digits + string.ascii_lowercase)


class MetaModel(models.Model):
    uuid = models.CharField(max_length=25, primary_key=True, default=normal_uuid.uuid)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='最后更新', auto_now=True, null=True)
    deleted_at = models.DateTimeField(verbose_name='删除时间', null=True)

    objects = models.Manager()

    class Meta:
        abstract = True


# 建档立卡: 客户资料, 用于后期进行合作挖掘
class Account(MetaModel):
    username = models.CharField(max_length=32, unique=True, verbose_name='客户称呼', null=False, blank=False)
    _mobile = models.CharField(max_length=64, unique=True, verbose_name='手机', null=True, blank=True)  # 需要脱敏保存
    email = models.EmailField(verbose_name='邮箱', blank=True, null=True)
    _wechat = models.CharField(verbose_name='微信', max_length=64, null=True, blank=True)
    qq = models.CharField(verbose_name='QQ', max_length=12, null=True, blank=True)
    git = models.URLField(verbose_name='git账户', null=True, blank=True)
    _id_card = models.CharField(verbose_name='身份证', null=True, blank=True, max_length=64)  # 需要脱敏保存
    annotation = models.TextField(verbose_name='备注', null=True, blank=True)
    source = models.CharField(verbose_name='客户来源', max_length=64, null=True, blank=True)

    class Meta:
        verbose_name_plural = verbose_name = '客户资料'
        db_table = 'account'
        app_label = 'xoo'

    def __str__(self):
        return self.username

    # 客户消费总金额
    def amount(self):
        return sum([ticket.number for ticket in self.tickets])

    # 客户订单数量
    def orders(self):
        return len(self.projetcs)

    # 明文电话号码
    def mobile(self):
        try:
            return aes.decrypt(self._mobile)
        except:
            return "188****8888"

    # 明文微信号码
    def wechat(self):
        try:
            return aes.decrypt(self._wechat)
        except:
            return ''

    # 明文身份证
    def id_card(self):
        try:
            return aes.decrypt(self._id_card)
        except:
            return ""


# 文件清单：关联需求文件等
class File(MetaModel):
    project = models.ForeignKey(to='Project', related_name='files', on_delete=models.CASCADE, verbose_name='所属项目',
                                null=True, blank=True)
    filename = models.FileField(upload_to='uploads/', null=True, blank=True, verbose_name='文件链接')

    class Meta:
        verbose_name_plural = verbose_name = '文件附件'
        db_table = 'file'
        app_label = 'xoo'

    def __str__(self):
        return self.filename.name


# 项目任务
class Project(MetaModel):
    name = models.CharField(verbose_name='项目名称', max_length=128)
    owner = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='projects', null=True, blank=True,
                              verbose_name='开发者')
    account = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='projects', null=True, blank=True,
                                verbose_name='客户')
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
        app_label = 'xoo'

    def __str__(self):
        return self.name

    # 实际收益金额
    def amount(self):
        return sum([ticket.number for ticket in self.tickets])


# 收款记录(账本): 支付宝红包口令即9位uuid
class Ticket(MetaModel):
    project = models.ForeignKey(to=Project, related_name='tickets', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='所属项目')
    account = models.ForeignKey(to=Account, related_name='tickets', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='客户')
    number = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='金额', default=0)
    annotation = models.CharField(max_length=64, verbose_name='备注', null=True, blank=True)
    validate_code = models.CharField(max_length=18, verbose_name='核销码', null=True, blank=True)
    validated_at = models.DateTimeField(verbose_name='核销时间', null=True)

    class Meta:
        verbose_name_plural = verbose_name = '收据'
        db_table = 'ticket'
        app_label = 'xoo'

    def __str__(self):
        return self.uuid
