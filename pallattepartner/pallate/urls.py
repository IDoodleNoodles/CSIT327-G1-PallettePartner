from django.urls import path
from . import views

app_name = 'pallate'

urlpatterns = [
    path('', views.index, name='index'),
]
