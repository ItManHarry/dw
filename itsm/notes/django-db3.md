# 数据库 - 3
### Search
1. Standard textual queries
> Text-based fields have a selection of matching operations. For example, you may wish to allow lookup up an author like so:
```bazaar
>>> Author.objects.filter(name__contains='Terry')
[<Author: Terry Gilliam>, <Author: Terry Jones>]
```
> This is a very fragile solution as it requires the user to know an exact substring of the author’s name. A better approach could be a case-insensitive match (icontains), but this is only marginally better.
2. A database’s more advanced comparison functions
> In the above example, we determined that a case insensitive lookup would be more useful. When dealing with non-English names, a further improvement is to use unaccented comparison:
```bazaar
>>> Author.objects.filter(name__unaccent__icontains='Helen')
[<Author: Helen Mirren>, <Author: Helena Bonham Carter>, <Author: Hélène Joy>]
```
> This shows another issue, where we are matching against a different spelling of the name. In this case we have an asymmetry though - a search for Helen will pick up Helena or Hélène, but not the reverse. Another option would be to use a trigram_similar comparison, which compares sequences of letters.
```bazaar
>>> Author.objects.filter(name__unaccent__lower__trigram_similar='Hélène')
[<Author: Helen Mirren>, <Author: Hélène Joy>]
```
3. Document-based search
> Standard database operations stop being a useful approach when you start considering large blocks of text. Whereas the examples above can be thought of as operations on a string of characters, full text search looks at the actual words. Depending on the system used, it’s likely to use some of the following ideas:
  - Ignoring “stop words” such as “a”, “the”, “and”.
  - Stemming words, so that “pony” and “ponies” are considered similar.
  - Weighting words based on different criteria such as how frequently they appear in the text, or the importance of the fields, such as the title or keywords, that they appear in.
### Managers
1. class Manager
> A Manager is the interface through which database query operations are provided to Django models. At least one Manager exists for every model in a Django application.
> The way Manager classes work is documented in Making queries; this document specifically touches on model options that customize Manager behavior.
2. Manager names
>   By default, Django adds a Manager with the name objects to every Django model class. However, if you want to use objects as a field name, or if you want to use a name other than objects for the Manager, you can rename it on a per-model basis. To rename the Manager for a given class, define a class attribute of type models.Manager() on that model. For example:
```bazaar
from django.db import models

class Person(models.Model):
    #...
    people = models.Manager()
```
> Using this example model, Person.objects will generate an AttributeError exception, but Person.people.all() will provide a list of all Person objects.
3. Custom managers
> You can use a custom Manager in a particular model by extending the base Manager class and instantiating your custom Manager in your model.
> There are two reasons you might want to customize a Manager: to add extra Manager methods, and/or to modify the initial QuerySet the Manager returns.
  - Adding extra manager methods
> Adding extra Manager methods is the preferred way to add “table-level” functionality to your models. (For “row-level” functionality – i.e., functions that act on a single instance of a model object – use Model methods, not custom Manager methods.)

> For example, this custom Manager adds a method with_counts():
```bazaar
from django.db import models
from django.db.models.functions import Coalesce

class PollManager(models.Manager):
    def with_counts(self):
        return self.annotate(
            num_responses=Coalesce(models.Count("response"), 0)
        )

class OpinionPoll(models.Model):
    question = models.CharField(max_length=200)
    objects = PollManager()

class Response(models.Model):
    poll = models.ForeignKey(OpinionPoll, on_delete=models.CASCADE)
    # ...
```
    1. A custom Manager method can return anything you want. It doesn’t have to return a QuerySet.
    2. Another thing to note is that Manager methods can access self.model to get the model class to which they’re attached.
  - Modifying a manager’s initial QuerySet
> You can override a Manager’s base QuerySet by overriding the Manager.get_queryset() method. get_queryset() should return a QuerySet with the properties you require.

>  For example, the following model has two Managers – one that returns all objects, and one that returns only the books by Roald Dahl:
```bazaar
# First, define the Manager subclass.
class DahlBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(author='Roald Dahl')

# Then hook it into the Book model explicitly.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)

    objects = models.Manager() # The default manager.
    dahl_objects = DahlBookManager() # The Dahl-specific manager.
```
> This example also pointed out another interesting technique: using multiple managers on the same model. You can attach as many Manager() instances to a model as you’d like. This is a non-repetitive way to define common “filters” for your models.
```bazaar
class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role='A')

class EditorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role='E')

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=1, choices=[('A', _('Author')), ('E', _('Editor'))])
    people = models.Manager()
    authors = AuthorManager()
    editors = EditorManager()
```
### Performing raw SQL queries
> Django gives you two ways of performing raw SQL queries: you can use Manager.raw() to perform raw queries and return model instances, or you can avoid the model layer entirely and execute custom SQL directly.
1. Performing raw queries
> The raw() manager method can be used to perform raw SQL queries that return model instances:
```bazaar
Manager.raw(raw_query, params=(), translations=None)
This method takes a raw SQL query, executes it, and returns a django.db.models.query.RawQuerySet instance. This RawQuerySet instance can be iterated over like a normal QuerySet to provide object instances
class Person(models.Model):
    first_name = models.CharField(...)
    last_name = models.CharField(...)
    birth_date = models.DateField(...)
>>> for p in Person.objects.raw('SELECT * FROM myapp_person'):
...     print(p)
John Smith
Jane Jones
```
2. Mapping query fields to model fields
> raw() automatically maps fields in the query to fields on the model.

>  The order of fields in your query doesn’t matter. In other words, both of the following queries work identically:
```bazaar
>>> Person.objects.raw('SELECT id, first_name, last_name, birth_date FROM myapp_person')
...
>>> Person.objects.raw('SELECT last_name, birth_date, first_name, id FROM myapp_person')
...
```
> Matching is done by name. This means that you can use SQL’s AS clauses to map fields in the query to model fields. So if you had some other table that had Person data in it, you could easily map it into Person instances:
```bazaar
>>> Person.objects.raw('''SELECT first AS first_name,
...                              last AS last_name,
...                              bd AS birth_date,
...                              pk AS id,
...                       FROM some_other_table''')
```
> As long as the names match, the model instances will be created correctly.

> Alternatively, you can map fields in the query to model fields using the translations argument to raw(). This is a dictionary mapping names of fields in the query to names of fields on the model. For example, the above query could also be written:
```bazaar
>>> name_map = {'first': 'first_name', 'last': 'last_name', 'bd': 'birth_date', 'pk': 'id'}
>>> Person.objects.raw('SELECT * FROM some_other_table', translations=name_map)
```
3. Index lookups
> raw() supports indexing, so if you need only the first result you can write:
```bazaar
>>> first_person = Person.objects.raw('SELECT * FROM myapp_person')[0]
```
> However, the indexing and slicing are not performed at the database level. If you have a large number of Person objects in your database, it is more efficient to limit the query at the SQL level:
```bazaar
>>> first_person = Person.objects.raw('SELECT * FROM myapp_person LIMIT 1')[0]
```
4. Deferring model fields
> Fields may also be left out:
```bazaar
>>> people = Person.objects.raw('SELECT id, first_name FROM myapp_person')
```
> The Person objects returned by this query will be deferred model instances (see defer()). This means that the fields that are omitted from the query will be loaded on demand. For example:
```bazaar
>>> for p in Person.objects.raw('SELECT id, first_name FROM myapp_person'):
...     print(p.first_name, # This will be retrieved by the original query
...           p.last_name) # This will be retrieved on demand
...
John Smith
Jane Jones
```
> From outward appearances, this looks like the query has retrieved both the first name and last name. However, this example actually issued 3 queries. Only the first names were retrieved by the raw() query – the last names were both retrieved on demand when they were printed. 
> There is only one field that you can’t leave out - the primary key field. Django uses the primary key to identify model instances, so it must always be included in a raw query. A FieldDoesNotExist exception will be raised if you forget to include the primary key.
5. Adding annotations
> You can also execute queries containing fields that aren’t defined on the model. For example, we could use PostgreSQL’s age() function to get a list of people with their ages calculated by the database:
```bazaar
>>> people = Person.objects.raw('SELECT *, age(birth_date) AS age FROM myapp_person')
>>> for p in people:
...     print("%s is %s." % (p.first_name, p.age))
John is 37.
Jane is 42.
...
```
6. Passing parameters into raw()
> If you need to perform parameterized queries, you can use the params argument to raw():
```bazaar
>>> lname = 'Doe'
>>> Person.objects.raw('SELECT * FROM myapp_person WHERE last_name = %s', [lname])
```
> params is a list or dictionary of parameters. You’ll use %s placeholders in the query string for a list, or %(key)s placeholders for a dictionary (where key is replaced by a dictionary key), regardless of your database engine. Such placeholders will be replaced with parameters from the params argument.
### Executing custom SQL directly
> The object django.db.connection represents the default database connection. To use the database connection, call connection.cursor() to get a cursor object. Then, call cursor.execute(sql, [params]) to execute the SQL and cursor.fetchone() or cursor.fetchall() to return the resulting rows.
```bazaar
from django.db import connection

def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()

    return row
```
> If you are using more than one database, you can use django.db.connections to obtain the connection (and cursor) for a specific database. django.db.connections is a dictionary-like object that allows you to retrieve a specific connection using its alias:
```bazaar
from django.db import connections
with connections['my_db_alias'].cursor() as cursor:
    # Your code here...
```
> By default, the Python DB API will return results without their field names, which means you end up with a list of values, rather than a dict. At a small performance and memory cost, you can return results as a dict by using something like this:
```bazaar
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
```
> Another option is to use collections.namedtuple() from the Python standard library. A namedtuple is a tuple-like object that has fields accessible by attribute lookup; it’s also indexable and iterable. Results are immutable and accessible by field names or indices, which might be useful:
```bazaar
from collections import namedtuple

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
```
### Connections and cursors
> If you’re not familiar with the Python DB-API, note that the SQL statement in cursor.execute() uses placeholders, "%s", rather than adding parameters directly within the SQL. If you use this technique, the underlying database library will automatically escape your parameters as necessary.
> Also note that Django expects the "%s" placeholder, not the "?" placeholder, which is used by the SQLite Python bindings. This is for the sake of consistency and sanity.
### Calling stored procedures
**CursorWrapper.callproc(procname, params=None, kparams=None)**
> Calls a database stored procedure with the given name. A sequence (params) or dictionary (kparams) of input parameters may be provided. Most databases don’t support kparams. Of Django’s built-in backends, only Oracle supports it.
> For example, given this stored procedure in an Oracle database:
```bazaar
CREATE PROCEDURE "TEST_PROCEDURE"(v_i INTEGER, v_text NVARCHAR2(10)) AS
    p_i INTEGER;
    p_text NVARCHAR2(10);
BEGIN
    p_i := v_i;
    p_text := v_text;
    ...
END;
```
> This will call it:
```bazaar
with connection.cursor() as cursor:
    cursor.callproc('test_procedure', [1, 'test'])
```
### Using raw cursors with multiple databases
> If you are using more than one database you can use django.db.connections to obtain the connection (and cursor) for a specific database. django.db.connections is a dictionary-like object that allows you to retrieve a specific connection using its alias:
```bazaar
from django.db import connections
with connections['my_db_alias'].cursor() as cursor:
    ...
```