from django.contrib import admin
from .models import ActionHistory


@admin.register(ActionHistory)
class ActionHistoryAdmin(admin.ModelAdmin):
    pass
