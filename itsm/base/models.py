from django.db import models
from django.utils import timezone
import time, datetime, uuid
# Base Model For All.
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
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)  # ID(自动生成UUID)
    active = models.BooleanField(default=True)                  # 是否有效(默认有效)
    created_on = models.DateTimeField(auto_now=True)            # 创建时间UAT
    created_by = models.CharField(max_length=32, null=True)     # 创建人
    updated_on = models.DateTimeField(default=timezone.now)     # 更新时间UAT
    updated_by = models.CharField(max_length=32, null=True)     # 更新人
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