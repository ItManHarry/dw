from django.db import models
class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    birth_date = models.DateField()

    def __str__(self):
        return self.first_name + self.last_name

    class Meta:
        db_table = 'stu_person'