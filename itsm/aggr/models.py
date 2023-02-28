from django.db import models
from django.db.models.functions import Coalesce
class Author(models.Model):
    name = models.CharField(max_length=64)
    age = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=256)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=256)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name
class PollManager(models.Manager):
    def with_counts(self):
        return self.annotate(num_responses=Coalesce(models.Count('response'), 0))
class OpinionPoll(models.Model):
    question = models.CharField(max_length=256)
    objects = PollManager()
    def __str__(self):
        return self.question

class Response(models.Model):
    poll = models.ForeignKey(OpinionPoll, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)
    def __str__(self):
        return self.content