from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin
class BizQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?'
    )
    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

class BizChoice(models.Model):
    question = models.ForeignKey(BizQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
class Log(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    question = models.ForeignKey(BizQuestion, on_delete=models.CASCADE)
    choice = models.ForeignKey(BizChoice, on_delete=models.CASCADE)
    log_date = models.DateTimeField('Choice time')
    remark = models.TextField(null=True)

    def __str__(self):
        return self.remark