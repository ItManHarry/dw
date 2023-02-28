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
  - A custom Manager method can return anything you want. It doesn’t have to return a QuerySet.
  - Another thing to note is that Manager methods can access self.model to get the model class to which they’re attached.