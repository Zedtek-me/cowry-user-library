from django.db import models

class BaseModel(models.Model):
    '''base model for all other models'''
    _id = models.AutoField(primary_key=True)
    meta = models.JSONField(default=dict)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["-_id", "-date_created", "-last_updated"]
        