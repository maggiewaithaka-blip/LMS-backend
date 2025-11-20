from django.db import models


class SystemConfig(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class Plugin(models.Model):
    name = models.CharField(max_length=255, unique=True)
    enabled = models.BooleanField(default=False)
    config = models.JSONField(default=dict, blank=True)
    installed_at = models.DateTimeField(auto_now_add=True)
