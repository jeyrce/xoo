from django.contrib import admin

from xoo import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
