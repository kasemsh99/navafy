from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.user_register),
    path('login/', views.user_login),
	path('user/', views.user_data),
	path('profile/edit/', views.profile_edit),

	path('artist/', views.artist_data),
	path('artist/edit/', views.artist_edit),

	path('search/', views.search),

	path('media/<int:media_id>/like/add/', views.add_like),
	path('media/liked/categorized/list/', views.categorized_liked_media),



]
