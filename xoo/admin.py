from django.contrib import admin

from xoo import models

admin.site.unregister(models.UserModel)
admin.site.site_header = '私活账本'


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(models.UserModel)
class SysUserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    pass


# 可能需要inline到account
@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass
