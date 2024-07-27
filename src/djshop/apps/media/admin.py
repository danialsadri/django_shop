from django.contrib import admin
from djshop.apps.media.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
