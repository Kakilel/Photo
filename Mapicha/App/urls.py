from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('upload/', views.upload_view, name='upload'),
    path('profile/', views.profile_view, name='profile'),
    path('category/', views.category_view, name='category'),
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),
    path('my_photos/', views.my_photos, name='my_photos'),
    path("photo/<int:photo_id>/like/", views.like_photo, name="like_photo"),
    path("photo/<int:photo_id>/comment/", views.add_comment, name="add_comment"),
]