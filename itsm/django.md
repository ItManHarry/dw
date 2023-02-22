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
```bazaar
    # option 'auto_now' means the columns won't be changed any more, option 'default' can be changed !
    create_date = models.DateField(auto_now=True)
    create_time = models.DateTimeField(auto_now=True)
    update_date = models.DateField(default=date.today)
    update_time = models.DateTimeField(default=timezone.now)
```
- Sample
```bazaar
from django.db import models
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```
2. Options
- null:If True, Django will store empty values as NULL in the database. Default is False
- blank:If True, the field is allowed to be blank. Default is False;Note that this is different than null. null is purely database-related, whereas blank is validation-related. If a field has blank=True, form validation will allow entry of an empty value. If a field has blank=False, the field will be required
- choices:A sequence of 2-tuples to use as choices for this field. If this is given, the default form widget will be a select box instead of the standard text field and will limit choices to the choices given
- default:The default value for the field. This can be a value or a callable object. If callable it will be called every time a new object is created
- help_text:Extra “help” text to be displayed with the form widget. It’s useful for documentation even if your field isn’t used on a form
- primary_key:If True, this field is the primary key for the model;If you don’t specify primary_key=True for any fields in your model, Django will automatically add an IntegerField to hold the primary key, so you don’t need to set primary_key=True on any of your fields unless you want to override the default primary-key behavior
- unique:If True, this field must be unique throughout the table
- verbose_name:Each field type, except for ForeignKey, ManyToManyField and OneToOneField, takes an optional first positional argument – a verbose name. If the verbose name isn’t given, Django will automatically create it using the field’s attribute name, converting underscores to spaces;ForeignKey, ManyToManyField and OneToOneField require the first argument to be a model class, so use the verbose_name keyword argument
3. 数据迁移
```bazaar
python manage.py makemigrations app-name
python manage.py migrate
```
