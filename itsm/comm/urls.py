from django.urls import path
from . import views
app_name = 'comm'
urlpatterns = [
    path('', views.index, name='index')
]