from django.db import models
from interfaces.models import BaseModel
from .constants import AVAILABLE, BORROWED, DELETED

class AdminBooksRepresentation(BaseModel):
    '''mocks/models the books on the admin side'''
    STATUSES = (
        (AVAILABLE, AVAILABLE),
        (DELETED, DELETED),
        (BORROWED, BORROWED)
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUSES, default=AVAILABLE)
    
