from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('face/', views.face_detection, name='face'),
    path('heart/', views.heart_rate_detection, name='heart'),
    path('heart_calc/', views.heart_rate_calculation, name='heart_calc'),
    path('upload/', views.file_upload, name='upload'),
    path('video/', views.video, name='video'),
    path('view/<str:pk>/', views.view_photo, name='view_photo'),
    path('detect/<str:pk>/', views.detect_faces, name="detect_faces"),
    path('delete/<str:pk>/', views.delete_photo, name="delete_photo"),
]