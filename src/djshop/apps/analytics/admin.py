from django.contrib import admin
from djshop.apps.analytics.models import ActionHistory


@admin.register(ActionHistory)
class ActionHistoryAdmin(admin.ModelAdmin):
    pass
