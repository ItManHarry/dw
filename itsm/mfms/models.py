from django.db import models
TITLE_CHOICES = [
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
]
class Author(models.Model):
    name = models.CharField(max_length=128)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.name
    @property
    def books(self):
        return [book for book in self.book_set.all()]
class Book(models.Model):
    name = models.CharField(max_length=128)
    authors = models.ManyToManyField(Author)
    def __str__(self):
        return self.name
    @property
    def get_authors(self):
        return [author for author in self.authors.all()]