from django.db import models
from datetime import date
from django.utils import timezone

class Dict(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField()
    created_by = models.CharField(max_length=32)
    updated_on = models.DateTimeField()
    updated_by = models.CharField(max_length=32)
    code = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=128)

class Enum(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=32)
    updated_on = models.DateTimeField()
    updated_by = models.CharField(max_length=32)
    code = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return 'Enum'+self.code

    class Meta:
        db_table = 'biz_enum'

class  FieldsPractise(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    is_active = models.BooleanField(default=True)
    create_date = models.DateField(auto_now=True)
    create_time = models.DateTimeField(auto_now=True)
    update_date = models.DateField(default=date.today)
    update_time = models.DateTimeField(default=timezone.now)