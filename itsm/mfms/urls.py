from django.urls import path
from . import views
app_name = 'mfms'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('author/index/', views.author_index, name='author_index'),
    path('author/add/', views.author_add, name='author_add'),
    path('author/edit/<id>', views.author_edit, name='author_edit'),
    path('book/index/', views.book_index, name='book_index'),
    path('book/add/', views.book_add, name='book_add'),
]