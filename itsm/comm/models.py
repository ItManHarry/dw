from django.db import models
from datetime import date
from django.utils import timezone

class Dict(models.Model):
    class Meta:
        db_table = 'sys_dict'
    id = models.CharField(max_length=32, primary_key=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=32)
    updated_on = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=32)
    code = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=128)
    def __str__(self):
        return 'Dictionary code {}, name {}.'.format(self.code, self.name)

class Enum(models.Model):
    class Meta:
        db_table = 'sys_enum'
    id = models.CharField(max_length=32, primary_key=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=32)
    updated_on = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=32)
    code = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=128)
    dictionary = models.ForeignKey(Dict, on_delete=models.CASCADE)

    def __str__(self):
        return 'Enumeration code {}, name {}.'.format(self.code, self.name)

class Employee(models.Model):
    class Meta:
        db_table = 'biz_employee'
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    id = models.CharField(max_length=32, primary_key=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=32)
    updated_on = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=32)
    code = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=128)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
    def __str__(self):
        return 'Employee name is {}, code {}, shirt size {}.'.format(self.name, self.code, self.get_shirt_size_display())

class  FieldsPractise(models.Model):
    class Meta:
        db_table = 'stu_practise'

    id = models.CharField(max_length=32, primary_key=True)
    is_active = models.BooleanField(default=True)
    create_date = models.DateField(auto_now=True)
    create_time = models.DateTimeField(auto_now=True)
    update_date = models.DateField(default=date.today)
    update_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id