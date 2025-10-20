from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'pallate'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='pallate:login'), name='logout'), 
    path('register/', views.register, name='register'),
    path('welcome/', views.welcome, name='welcome'),
    path('account/', views.account, name='account'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('artist-profile/', views.artist_profile, name='artist_profile'),
    path('collaboration-detail/', views.collaboration_detail, name='collaboration_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('collaboration/<int:pk>/messages/', views.collab_messages, name='collab_messages'),

]