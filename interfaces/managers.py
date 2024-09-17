from django.db import models

class BaseManager(models.Manager):
    '''base manager for all other managers'''

    def get_queryset(self):
        super().get_queryset().exclude(deleted_at__isnull=False)
