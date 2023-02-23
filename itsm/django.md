# 虚拟环境Conda
1. 安装&配置
    官网地址：https://conda.io/projects/conda/en/latest/user-guide/install/index.html
2. 常用命令
   - 查看版本：conda --version
   - 升级版本：conda update conda
   - 创建虚拟环境：conda create --name 'env-name' python=3.11 (指定虚机环境python版本)
   - 激活虚拟环境：conda activate 'env-name' 
   - 查看虚拟环境清单：conda info --envs
   - 网址：https://conda.io/projects/conda/en/latest/user-guide/getting-started.html
# Django 4.0
## 安装（使用pip）
```bazaar
pip install django -i https://pypi.tuna.tsinghua.edu.cn/simple
```    
## Django命令
### Django Basic
1. 创建工程：
```bazaar
django-admin startprojects project-name
```
2. 工程文件目录

| 文件/目录                | 说明                                                                                                                                                                                     |
|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| manage.py            | A command-line utility that lets you interact with this Django project in various ways. You can read all the details about manage.py in django-admin and manage.py                     |
| pro-name(文件夹)        | The inner pro-name/ directory is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. pro-name.urls). |
| pro-name/__init__.py | package remark                                                                                                                                                                         |
| pro-name/asgi.py     | An entry-point for ASGI-compatible web servers to serve your project. See How to deploy with ASGI for more details.                                                                    |
| pro-name/wsgi.py     | An entry-point for WSGI-compatible web servers to serve your project. See How to deploy with WSGI for more details.                                                                    |
| pro-name/urls.py     | The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in URL dispatcher.                                       |
| pro-name/settings.py | Settings/configuration for this Django project. Django settings will tell you all about how settings work                                                                              |
3. 启动工程
```bazaar
python manage.py runserver 8080
```
4. 创建模块
```bazaar
python manage.py startapp app-name
```
App目录：

| 文件/目录            | 说明                               |
|------------------|----------------------------------|
| __init__.pyt     | 包初始化文件                           |
| admin.py         | 注册模型                             |
| apps.py          | 注册模块（settings.py INSTALLED_APPS） |
| models.py        | 数据库模型                            |
| tests.py         | 单元测试                             |
| urls.py(自创建)     | 路由注册                             |
| views.py         | 视图action                         |
| migrations       | 模型迁移                             |
| static(自创建，也可全局) | 静态资源文件                           |
| templates(自创建，也可全局)        | 视图模板                             |

### 数据库
1. 数据模型
- Each model is a Python class that subclasses django.db.models.Model
- Each attribute of the model represents a database field
- With all of this, Django gives you an automatically-generated database-access API; see Making queries
- Table name：it is automatically derived from some model metadata but can be overridden(defaults:myapp_person)
- To override the database table name, use the db_table parameter in class Meta
- Date&DateTime Columns:
- Sample
```bazaar
from django.db import models
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # option 'auto_now' means the columns won't be changed any more, option 'default' can be changed !
    create_date = models.DateField(auto_now=True)
    create_time = models.DateTimeField(auto_now=True)
    update_date = models.DateField(default=date.today)
    update_time = models.DateTimeField(default=timezone.now)
```
2. Options
- **null**:If True, Django will store empty values as NULL in the database. Default is False
- **blank**:If True, the field is allowed to be blank. Default is False;Note that this is different than null. null is purely database-related, whereas blank is validation-related. If a field has blank=True, form validation will allow entry of an empty value. If a field has blank=False, the field will be required
- **choices**:A sequence of 2-tuples to use as choices for this field. If this is given, the default form widget will be a select box instead of the standard text field and will limit choices to the choices given
- **default**:The default value for the field. This can be a value or a callable object. If callable it will be called every time a new object is created
- **help_text**:Extra “help” text to be displayed with the form widget. It’s useful for documentation even if your field isn’t used on a form
- **primary_key**:If True, this field is the primary key for the model;If you don’t specify primary_key=True for any fields in your model, Django will automatically add an IntegerField to hold the primary key, so you don’t need to set primary_key=True on any of your fields unless you want to override the default primary-key behavior
- **unique**:If True, this field must be unique throughout the table
- **verbose_nam**:Each field type, except for ForeignKey, ManyToManyField and OneToOneField, takes an optional first positional argument – a verbose name. If the verbose name isn’t given, Django will automatically create it using the field’s attribute name, converting underscores to spaces;ForeignKey, ManyToManyField and OneToOneField require the first argument to be a model class, so use the verbose_name keyword argument
3. 数据迁移
```bazaar
python manage.py makemigrations app-name
python manage.py migrate
```
4. 数据操作
- 创建数据模型
> To represent database-table data in Python objects, Django uses an intuitive system: A model class represents a database table, and an instance of that class represents a particular record in the database table.
```bazaar
from datetime import date

from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.headline
```
- 保存数据（新增/修改）：
> To create an object, instantiate it using keyword arguments to the model class, then call save() to save it to the database.
```bazaar
>>> from blog.models import Blog
>>> b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
>>> b.save()
```
> To save changes to an object that’s already in the database, use save()
```bazaar
>>> b5.name = 'New name'
>>> b5.save()
```
> This performs an UPDATE SQL statement behind the scenes. Django doesn’t hit the database until you explicitly call save().
- Saving ForeignKey and ManyToManyField fields
> Updating a ForeignKey field works exactly the same way as saving a normal field – assign an object of the right type to the field in question. This example updates the blog attribute of an Entry instance entry, assuming appropriate instances of Entry and Blog are already saved to the database (so we can retrieve them below):
```bazaar
>>> from blog.models import Blog, Entry
>>> entry = Entry.objects.get(pk=1)
>>> cheese_blog = Blog.objects.get(name="Cheddar Talk")
>>> entry.blog = cheese_blog
>>> entry.save()
```
> Updating a ManyToManyField works a little differently – use the add() method on the field to add a record to the relation. This example adds the Author instance joe to the entry object:
```bazaar
>>> from blog.models import Author
>>> joe = Author.objects.create(name="Joe")
>>> entry.authors.add(joe)
```
> To add multiple records to a ManyToManyField in one go, include multiple arguments in the call to add(), like this:
```bazaar
>>> john = Author.objects.create(name="John")
>>> paul = Author.objects.create(name="Paul")
>>> george = Author.objects.create(name="George")
>>> ringo = Author.objects.create(name="Ringo")
>>> entry.authors.add(john, paul, george, ringo)
```
5. 数据查询
- Retrieve all data
```bazaar
>>> all_entries = Entry.objects.all()
```
- Retrieving specific objects with filters
> The QuerySet returned by all() describes all objects in the database table. Usually, though, you’ll need to select only a subset of the complete set of objects.
> To create such a subset, you refine the initial QuerySet, adding filter conditions. The two most common ways to refine a QuerySet are:
  1. filter(**kwargs)
  > Returns a new QuerySet containing objects that match the given lookup parameters.
  2. exclude(**kwargs)
  > Returns a new QuerySet containing objects that do not match the given lookup parameters.
```bazaar
Entry.objects.filter(pub_date__year=2006)
# same as 
Entry.objects.all().filter(pub_date__year=2006)
```
- Chaining filters
> The result of refining a QuerySet is itself a QuerySet, so it’s possible to chain refinements together. For example:
```bazaar
>>> Entry.objects.filter(
...     headline__startswith='What'
... ).exclude(
...     pub_date__gte=datetime.date.today()
... ).filter(
...     pub_date__gte=datetime.date(2005, 1, 30)
... )
```
- QuerySets are lazy
> QuerySets are lazy – the act of creating a QuerySet doesn’t involve any database activity. You can stack filters together all day long, and Django won’t actually run the query until the QuerySet is evaluated. Take a look at this example:
```bazaar
>>> q = Entry.objects.filter(headline__startswith="What")
>>> q = q.filter(pub_date__lte=datetime.date.today())
>>> q = q.exclude(body_text__icontains="food")
>>> print(q)
```
> Though this looks like three database hits, in fact it hits the database only once, at the last line (print(q)). In general, the results of a QuerySet aren’t fetched from the database until you “ask” for them. When you do, the QuerySet is evaluated by accessing the database. For more details on exactly when evaluation takes place, see When QuerySets are evaluated.
- Retrieving a single object with get()
> filter() will always give you a QuerySet, even if only a single object matches the query - in this case, it will be a QuerySet containing a single element.
```bazaar
>>> one_entry = Entry.objects.get(pk=1)
```
- Limiting QuerySets
> Use a subset of Python’s array-slicing syntax to limit your QuerySet to a certain number of results. This is the equivalent of SQL’s LIMIT and OFFSET clauses.
> For example, this returns the first 5 objects (LIMIT 5):
```bazaar
>>> Entry.objects.all()[:5]
>>> Entry.objects.all()[5:10]
```
- Field Lookup
> Field lookups are how you specify the meat of an SQL WHERE clause. They’re specified as keyword arguments to the QuerySet methods filter(), exclude() and get().
> Basic lookups keyword arguments take the form field__lookuptype=value. (That’s a double-underscore). For example:
```bazaar
>>> Entry.objects.filter(pub_date__lte='2006-01-01')
```
> translates (roughly) into the following SQL:
```bazaar
SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';
```
  - exact(equal to '=')
```bazaar
# SELECT ... WHERE headline = 'Cat bites dog';
>>> Entry.objects.get(headline__exact="Cat bites dog")
>>> Blog.objects.get(id__exact=14)  # Explicit form
>>> Blog.objects.get(id=14)         # __exact is implied
```
  - iexact(忽略大小写)
```bazaar
>>> Blog.objects.get(name__iexact="beatles blog")
```
> Would match a Blog titled "Beatles Blog", "beatles blog", or even "BeAtlES blOG".
  - contains(like, case-sensitive)
```bazaar
# SELECT ... WHERE headline LIKE '%Lennon%';
Entry.objects.get(headline__contains='Lennon')
```
  - icontains(like, case-insensitive)
```bazaar
# SELECT ... WHERE headline LIKE '%lennon%';
Entry.objects.get(headline__contains='lennon')
```
  - startswith/istartswith
```bazaar
# SELECT ... WHERE headline LIKE '%lennon';
Entry.objects.get(headline__startswith='lennon')
```
  - endswith/iendwith
```bazaar
# SELECT ... WHERE headline LIKE 'lennon%';
Entry.objects.get(headline__endswith='lennon')
```
[QuerySet API reference](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#field-lookups)
- Lookups that span relationships
> Django offers a powerful and intuitive way to “follow” relationships in lookups, taking care of the SQL JOINs for you automatically, behind the scenes. To span a relationship, use the field name of related fields across models, separated by double underscores, until you get to the field you want.
- Filters can reference fields on the model
> Django provides F expressions to allow such comparisons. Instances of F() act as a reference to a model field within a query. These references can then be used in query filters to compare the values of two different fields on the same model instance.
> For example, to find a list of all blog entries that have had more comments than pingbacks, we construct an F() object to reference the pingback count, and use that F() object in the query:
```bazaar
>>> from django.db.models import F
>>> Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks'))
```
