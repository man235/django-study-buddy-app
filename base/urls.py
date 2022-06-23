from django.urls import path
from . import views


urlpatterns = [
    # name: double quotation marks
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
]