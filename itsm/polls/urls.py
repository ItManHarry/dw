from django.urls import path, re_path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    re_path('(\d+)', views.reg_demo, name='reg_demo'),
    path('reverse/', views.reverse_handler, name='reverse'),
    path('json/', views.json_resp, name='json_resp'),
    path('home/', views.home, name='home')
]