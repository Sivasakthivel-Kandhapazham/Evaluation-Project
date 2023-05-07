from django.urls import path
from . import views


urlpatterns = [
    path('image_gallery', views.image_gallery_view, name="image_gallery"),
    path('image_upload', views.image_upload_view, name="image_upload"),
    path('post_image', views.upload_image_process, name = 'post_image'),
    path('image_summary/<int:id>', views.image_detailed_view, name="image_summary"),
    path('image_search', views.image_gallery_filter, name = 'image_search'),
    path('logout', views.logout, name = "logout"),
]