from django.urls import path

from . import views

app_name = 'spider'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('query', views.query, name='query'),
]
