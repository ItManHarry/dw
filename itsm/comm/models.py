from django.db import models

class Dict(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField()
    created_by = models.CharField(max_length=32)
    updated_on = models.DateTimeField()
    updated_by = models.CharField(max_length=32)
    code = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=128)
