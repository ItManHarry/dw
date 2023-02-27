# 数据库 - 2
### Aggregation
```bazaar
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

class Publisher(models.Model):
    name = models.CharField(max_length=300)

class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()

class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)
    
# Total number of books.
>>> Book.objects.count()
2452

# Total number of books with publisher=BaloneyPress
>>> Book.objects.filter(publisher__name='BaloneyPress').count()
73

# Average price across all books.
>>> from django.db.models import Avg
>>> Book.objects.aggregate(Avg('price'))
{'price__avg': 34.35}

# Max price across all books.
>>> from django.db.models import Max
>>> Book.objects.aggregate(Max('price'))
{'price__max': Decimal('81.20')}

# Difference between the highest priced book and the average price of all books.
>>> from django.db.models import FloatField
>>> Book.objects.aggregate(
...     price_diff=Max('price', output_field=FloatField()) - Avg('price'))
{'price_diff': 46.85}

# All the following queries involve traversing the Book<->Publisher
# foreign key relationship backwards.

# Each publisher, each with a count of books as a "num_books" attribute.
>>> from django.db.models import Count
>>> pubs = Publisher.objects.annotate(num_books=Count('book'))
>>> pubs
<QuerySet [<Publisher: BaloneyPress>, <Publisher: SalamiPress>, ...]>
>>> pubs[0].num_books
73

# Each publisher, with a separate count of books with a rating above and below 5
>>> from django.db.models import Q
>>> above_5 = Count('book', filter=Q(book__rating__gt=5))
>>> below_5 = Count('book', filter=Q(book__rating__lte=5))
>>> pubs = Publisher.objects.annotate(below_5=below_5).annotate(above_5=above_5)
>>> pubs[0].above_5
23
>>> pubs[0].below_5
12

# The top 5 publishers, in order by number of books.
>>> pubs = Publisher.objects.annotate(num_books=Count('book')).order_by('-num_books')[:5]
>>> pubs[0].num_books
1323
```
### Generating aggregates over a QuerySet
> Django provides two ways to generate aggregates. The first way is to generate summary values over an entire QuerySet. 
```bazaar
>>> Book.objects.all()
#What we need is a way to calculate summary values over the objects that belong to this QuerySet. This is done by appending an aggregate() clause onto the QuerySet:
>>> from django.db.models import Avg
>>> Book.objects.all().aggregate(Avg('price'))
{'price__avg': 34.35}
#The all() is redundant in this example, so this could be simplified to:
>>> Book.objects.aggregate(Avg('price'))
{'price__avg': 34.35}
```
> aggregate() is a terminal clause for a QuerySet that, when invoked, returns a dictionary of name-value pairs. The name is an identifier for the aggregate value; the value is the computed aggregate. The name is automatically generated from the name of the field and the aggregate function. If you want to manually specify a name for the aggregate value, you can do so by providing that name when you specify the aggregate clause:
```bazaar
>>> Book.objects.aggregate(average_price=Avg('price'))
{'average_price': 34.35}
```
> If you want to generate more than one aggregate, you add another argument to the aggregate() clause. So, if we also wanted to know the maximum and minimum price of all books, we would issue the query:'
```bazaar
>>> from django.db.models import Avg, Max, Min
>>> Book.objects.aggregate(Avg('price'), Max('price'), Min('price'))
{'price__avg': 34.35, 'price__max': Decimal('81.20'), 'price__min': Decimal('12.99')}
```
### Generating aggregates for each item in a QuerySet
> The second way to generate summary values is to generate an independent summary for each object in a QuerySet. For example, if you are retrieving a list of books, you may want to know how many authors contributed to each book. Each Book has a many-to-many relationship with the Author; we want to summarize this relationship for each book in the QuerySet.
> Per-object summaries can be generated using the annotate() clause. When an annotate() clause is specified, each object in the QuerySet will be annotated with the specified values.
> The syntax for these annotations is identical to that used for the aggregate() clause. Each argument to annotate() describes an aggregate that is to be calculated. For example, to annotate books with the number of authors
```bazaar
# Build an annotated queryset
>>> from django.db.models import Count
>>> q = Book.objects.annotate(Count('authors'))
# Interrogate the first object in the queryset
>>> q[0]
<Book: The Definitive Guide to Django>
>>> q[0].authors__count
2
# Interrogate the second object in the queryset
>>> q[1]
<Book: Practical Django Projects>
>>> q[1].authors__count
1
```
> As with aggregate(), the name for the annotation is automatically derived from the name of the aggregate function and the name of the field being aggregated. You can override this default name by providing an alias when you specify the annotation:
```bazaar
>>> q = Book.objects.annotate(num_authors=Count('authors'))
>>> q[0].num_authors
2
>>> q[1].num_authors
1
```
### Combining multiple aggregations
> Combining multiple aggregations with annotate() will yield the wrong results because joins are used instead of subqueries:
```bazaar
>>> book = Book.objects.first()
>>> book.authors.count()
2
>>> book.store_set.count()
3
>>> q = Book.objects.annotate(Count('authors'), Count('store'))
>>> q[0].authors__count
6
>>> q[0].store__count
6
```
> For most aggregates, there is no way to avoid this problem, however, the Count aggregate has a distinct parameter that may help:
```bazaar
>>> q = Book.objects.annotate(Count('authors', distinct=True), Count('store', distinct=True))
>>> q[0].authors__count
2
>>> q[0].store__count
3
```
### Joins and aggregates
> So far, we have dealt with aggregates over fields that belong to the model being queried. However, sometimes the value you want to aggregate will belong to a model that is related to the model you are querying.
> When specifying the field to be aggregated in an aggregate function, Django will allow you to use the same double underscore notation that is used when referring to related fields in filters. Django will then handle any table joins that are required to retrieve and aggregate the related value.
> For example, to find the price range of books offered in each store, you could use the annotation:
```bazaar
>>> from django.db.models import Max, Min
>>> Store.objects.annotate(min_price=Min('books__price'), max_price=Max('books__price'))
```
> The same rules apply to the aggregate() clause. If you wanted to know the lowest and highest price of any book that is available for sale in any of the stores, you could use the aggregate:
```bazaar
>>> Store.objects.aggregate(min_price=Min('books__price'), max_price=Max('books__price'))
```
> Join chains can be as deep as you require. For example, to extract the age of the youngest author of any book available for sale, you could issue the query:
```bazaar
>>> Store.objects.aggregate(youngest_age=Min('books__authors__age'))
```
### Following relationships backwards
> In a way similar to Lookups that span relationships, aggregations and annotations on fields of models or models that are related to the one you are querying can include traversing “reverse” relationships. The lowercase name of related models and double-underscores are used here too.
> For example, we can ask for all publishers, annotated with their respective total book stock counters (note how we use 'book' to specify the Publisher -> Book reverse foreign key hop):
```bazaar
>>> from django.db.models import Avg, Count, Min, Sum
>>> Publisher.objects.annotate(Count('book'))
#We can also ask for the oldest book of any of those managed by every publisher:
>>> Publisher.objects.aggregate(oldest_pubdate=Min('book__pubdate'))
```
> This doesn’t apply just to foreign keys. It also works with many-to-many relations. For example, we can ask for every author, annotated with the total number of pages considering all the books the author has (co-)authored (note how we use 'book' to specify the Author -> Book reverse many-to-many hop):
```bazaar
>>> Author.objects.annotate(total_pages=Sum('book__pages'))
```
