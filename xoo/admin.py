import datetime

from django.contrib import admin

from xoo import models

admin.site.unregister(models.UserModel)
admin.site.site_header = '秀哦工作室'
meta_fields = ('uuid', 'created_at', 'updated_at', 'deleted_at')


# 公共类
class BaseAdmin(admin.ModelAdmin):
    list_per_page = 100

    def delete_model(self, request, obj):
        obj.deleted_at = datetime.datetime.now()
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(deleted_at=None)

    def has_view_permission(self, request, obj=None):
        if request.is_superuser:
            return True
        if obj and request.user.is_active:
            return request.user.pk == obj.owner.pk
        return super().has_change_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj and request.user.is_active:
            return request.user.pk == obj.owner.pk
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and request.user.is_active:
            return request.user.pk == obj.owner.pkt


class FilesInline(admin.StackedInline):
    model = models.File
    can_delete = True


@admin.register(models.Project)
class ProjectAdmin(BaseAdmin):
    """"""
    list_display = ('name', 'owner', 'account', 'days', 'price', 'amount', 'created_at', 'finished', 'online_url')
    list_editable = ('name', 'account', 'finished', 'online_url')
    readonly_fields = ('amount',) + meta_fields
    ordering = ('-created_at',)
    search_fields = ('name', 'owner_username', 'account_username')
    list_filter = ('finished',)
    inlines = (FilesInline,)
    fieldsets = (
        ('基本信息', {'fields': ('name', 'account', 'price'), },),
        ('项目明细', {'fields': ('detail',), },),
        ('项目地址', {'fields': ('code_hub', 'image_hub', 'online_url'), },)
    )

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        obj.save()


@admin.register(models.UserModel)
class SysUserAdmin(BaseAdmin):
    list_display = ('username', 'email', 'last_login', 'is_superuser', 'is_active')
    list_editable = ('is_superuser', 'is_active')
    ordering = ('-date_joined',)
    search_fields = ('username', 'email',)
    list_filter = ('is_active', 'is_superuser',)


@admin.register(models.Account)
class AccountAdmin(BaseAdmin):
    list_display = ('username', 'email', 'source', 'orders', 'amount', 'annotation')
    readonly_fields = ('amount', 'orders') + meta_fields
    list_editable = ('annotation',)
    ordering = ('-created_at',)
    search_fields = ('username', 'annotation')


@admin.register(models.Ticket)
class TicketAdmin(BaseAdmin):
    list_display = ('project', 'account', 'number', 'validate_code', 'annotation', 'created_at')
    list_editable = ('annotation',)
    readonly_fields = meta_fields
    ordering = ('-created_at',)
    search_fields = ('project__name', 'account__username', 'number',)
