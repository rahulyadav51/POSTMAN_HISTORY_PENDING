### models.py

from django.db import models

class APIRequestHistory(models.Model):
    url = models.URLField()
    method = models.CharField(max_length=10)
    headers = models.TextField(blank=True)
    body_type = models.CharField(max_length=50, default='none')
    raw_body = models.TextField(blank=True, null=True)
    formdata = models.JSONField(blank=True, null=True)
    urlencoded = models.JSONField(blank=True, null=True)
    response_body = models.TextField(blank=True, null=True)
    status_code = models.IntegerField(blank=True, null=True)
    time_elapsed = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

