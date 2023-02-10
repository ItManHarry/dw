from django.db import models
from django.utils import timezone
class BaseModel(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now())
    created_by = models.CharField(max_length=32)
    updated_on = models.DateTimeField(default=timezone.now())
    updated_by = models.CharField(max_length=32)