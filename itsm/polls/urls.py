from django.urls import path, re_path
from . import views
app_name = 'polls'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    # path('<int:question_id>/', views.detail, name='detail'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:question_id>/results/', views.results, name='results'),
    path('<int:pk>/results/', views.ResultView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # re_path('(\d+)', views.reg_demo, name='reg_demo'),
    path('reverse/', views.reverse_handler, name='reverse'),
    path('json/', views.json_resp, name='json_resp'),
    path('home/', views.home, name='home'),
    path('upload/', views.upload_file, name='upload'),
    path('uploads/', views.upload_files, name='uploads'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    # path('multiple/', views.FileFieldFormView.as_view(), name='multiple_upload'),
]