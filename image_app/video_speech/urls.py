from django.urls import path
from . import views


urlpatterns = [
    path('video_text', views.video_text_view, name = "video_text"),
    path('post_video', views.upload_video_process, name = 'post_video')
]