from django.urls import path
from . import views
app_name = 'frms'
urlpatterns = [
    path('', views.index, name='index')
]