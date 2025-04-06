### models.py

from django.db import models

class APIRequestHistory(models.Model):
    url = models.TextField()
    method = models.CharField(max_length=10)
    headers = models.TextField(blank=True)
    body_type = models.CharField(max_length=30)
    raw_body = models.TextField(blank=True, null=True)
    formdata = models.JSONField(blank=True, null=True)
    urlencoded = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.url} @ {self.timestamp}"
