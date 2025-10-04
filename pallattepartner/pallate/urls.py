from django.urls import path
from . import views

app_name = 'pallate'

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('artist-profile/', views.artist_profile, name='artist_profile'),
    path('collaboration-detail/', views.collaboration_detail, name='collaboration_detail'),
]
