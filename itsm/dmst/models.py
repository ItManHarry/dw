from django.db import models
from datetime import date
from django.utils import timezone
import time, datetime, uuid
'''
Abstract base classes are useful when you want to put some common information into 
a number of other models. You write your base class and put abstract=True in the Meta class. 
This model will then not be used to create any database table. Instead, when it is used as 
a base class for other models, its fields will be added to those of the child class
'''
class BaseModel(models.Model):
    class Meta:
        abstract = True
    # 表共同栏位
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)     # ID(自动生成UUID)
    active = models.BooleanField(default=True)                                      # 是否有效(默认有效)
    created_on = models.DateTimeField(auto_now=True)                                # 创建时间UAT
    created_by = models.CharField(max_length=32, null=True)                         # 创建人
    updated_on = models.DateTimeField(default=timezone.now)                         # 更新时间UAT
    updated_by = models.CharField(max_length=32, null=True)                         # 更新人
    #
    def created_on_locale(self, off_set=None):
        return self.utc_to_locale(self.created_on, off_set)

    def updated_on_locale(self, off_set=None):
        return self.utc_to_locale(self.updated_on, off_set)

    def utc_to_locale(self, utc_date_time, off_set=None):
        '''
        UTC时间转本地
        :param utc_date_time:   UTC时间
        :param off_set:         时区(如果为None则默认转为本地时区)
        :return:
        '''
        now_stamp = time.time()
        locale_time = datetime.datetime.fromtimestamp(now_stamp)
        utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
        # 计算时区差
        if off_set is None:
            off_set = locale_time - utc_time
        else:
            off_set = datetime.timedelta(hours=off_set)
        locale_date_time = utc_date_time + off_set
        return locale_date_time
'''
Many to One
'''
class Factory(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=32)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Car(models.Model):
    model = models.CharField(max_length=24)
    serial_no = models.CharField(max_length=32)
    active = models.BooleanField(default=True)
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)

    def __str__(self):
        return self.model
class Reporter(BaseModel):
    name = models.CharField(max_length=32)
    id_card = models.CharField(max_length=24)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = 'biz_reporter'

class Article(BaseModel):
    headline = models.CharField(max_length=256)
    pub_date = models.DateField(default=date.today)
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline

    class Meta(BaseModel.Meta):
        db_table = 'biz_article'
        ordering = ['-pub_date']
class Department(BaseModel):
    code = models.CharField(max_length=24)
    name = models.CharField(max_length=256)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    @property
    def children(self):
        return Department.objects.filter(parent_id=self.id)
    def __str__(self):
        return self.name
    class Meta(BaseModel.Meta):
        db_table = 'biz_department'
'''
Many to Many
'''
class Musician(BaseModel):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
    class Meta(BaseModel.Meta):
        db_table = 'biz_musician'

class Band(BaseModel):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Musician, through='BandShip')
    def __str__(self):
        return self.name
    class Meta(BaseModel.Meta):
        db_table = 'biz_band'
class BandShip(BaseModel):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    joined_date = models.DateField()
    remark = models.CharField(max_length=256)
    class Meta(BaseModel.Meta):
        db_table = 'rel_band_musician'

'''
One to One 
'''
class Capital(BaseModel):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = 'biz_capital'

class Country(BaseModel):
    name = models.CharField(max_length=64)
    capital = models.OneToOneField(Capital, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def full_str(self):
        return 'Country is {}, capital is {}.'.format(self.name, self.capital)

    class Meta(BaseModel.Meta):
        db_table = 'biz_country'

'''
Multi-table inheritance¶
The second type of model inheritance supported by Django is when each model in 
the hierarchy is a model all by itself. Each model corresponds to its own database 
table and can be queried and created individually. The inheritance relationship 
introduces links between the child model and each of its parents (via an automatically-created 
OneToOneField). For example:
'''
class Place(BaseModel):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = 'biz_place'

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    class Meta(Place.Meta):
        db_table = 'biz_restaurant'

'''
Proxy models¶
When using multi-table inheritance, a new database table is created for each 
subclass of a model. This is usually the desired behavior, since the subclass 
needs a place to store any additional data fields that are not present on the 
base class. Sometimes, however, you only want to change the Python behavior of 
a model – perhaps to change the default manager, or add a new method.
This is what proxy model inheritance is for: creating a proxy for the original model. 
You can create, delete and update instances of the proxy model and all the data will 
be saved as if you were using the original (non-proxied) model. The difference is that 
you can change things like the default model ordering or the default manager in the proxy, 
without having to alter the original.

Proxy models are declared like normal models. You tell Django that it’s a proxy model 
by setting the proxy attribute of the Meta class to True.
'''
class Person(BaseModel):
    name = models.CharField(max_length=64)
    age = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = 'biz_person'
class ProxyPerson(Person):
    class Meta(Person.Meta):
        proxy = True
        ordering = ['age']
