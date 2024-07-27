from django.contrib.admin.models import LogEntry


class ActionHistory(LogEntry):
    class Meta:
        proxy = True
