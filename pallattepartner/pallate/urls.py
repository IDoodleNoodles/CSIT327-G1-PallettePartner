from django.urls import path
from . import views

app_name = 'pallate'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('welcome/', views.welcome, name='welcome'),
    path('account/', views.account, name='account'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('artist-profile/', views.artist_profile, name='artist_profile'),
    path('collaboration-detail/', views.collaboration_detail, name='collaboration_detail'),
]
