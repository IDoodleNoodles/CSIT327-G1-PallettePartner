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
    path('artist-profile/', views.artist_profile, name='artist_profile'),  # supports ?user=
    path('artist/<int:user_id>/', views.artist_profile, name='artist_profile_by_id'),
    path('collaboration-detail/', views.collaboration_detail, name='collaboration_detail_legacy'),
    path('collaboration/<int:pk>/', views.collaboration_detail, name='collaboration_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('favorites/', views.favorites, name='favorites'),
    path('upload-artwork/', views.upload_artwork, name='upload_artwork'),
    path('toggle-favorite/<int:artwork_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('collaboration/<int:pk>/messages/', views.collab_messages, name='collab_messages'),
]