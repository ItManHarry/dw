from django.contrib import admin

# Register your models here.
from .models import Dict, Enum
admin.site.register(Dict)
admin.site.register(Enum)
