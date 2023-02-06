from django.contrib import admin

# Register your models here.
from . models import BizQuestion, BizChoice
admin.site.register(BizQuestion)
admin.site.register(BizChoice)
