from django.urls import path
from . import views

app_name = 'pallate'

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
