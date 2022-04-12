from turtle import home
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home,name="home"),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerPage,name='register'),
    path('room/<str:pk>/', views.room,name="room"),
    path('profile/<str:pk>/', views.userProfile,name="user-Profile"),
    path('create-room/', views.createRoom,name="create-room"),
    path('update-room/<str:pk>/',views.updateRoom,name="update-room"),
    path('delete-room/<str:pk>/',views.deleteRoom,name="delete-room"),
    path('delete-message/<str:pk>/',views.deleteMessage,name="delete-message"),
    path('topics',views.topicsPage,name="topics"),
    path('activity',views.activityPage,name="activity"),
    path('update_user',views.updateUser,name="update_user")
]
