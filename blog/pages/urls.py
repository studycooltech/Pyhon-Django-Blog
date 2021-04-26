from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('single/post/<slug:slug>/<int:id>', views.single_post,name='single_post'),
    path('register', views.user_reg,name='user_reg'),
    path('login', views.user_login,name='user_login'),
    path('post/publish', views.post_publish,name='post_publish'),
    path('update/<int:id>', views.posts_update, name='update'),
    path('delete/<int:id>', views.posts_delete, name='delete'),
    path('profile', views.profile,name='profile'),
    path('profile-edit/', views.profile_edit, name='profile-edit'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('logout', views.user_logout,name='user_logout'),
    path('profile-create/', views.profile_create, name='profile-create'),
    path('like/', views.like, name='like'),
    path('search/', views.search, name = 'search'),
    path('subscribe/',views.subscribe, name='subscribe'),
    path('contact/',views.contact, name='contact'),
    path('add/', views.addPhoto, name='add'),
   
]