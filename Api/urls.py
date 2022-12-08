from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.user_register),
    path('login/', views.user_login),
	path('user/', views.user_data),
	path('profile/edit/', views.profile_edit),

	path('artist/', views.artist_data),
	path('artist/edit/', views.artist_edit),

	path('favorite/create/', views.favorite_create),
	path('favorite/<int:favorite_id>/media/add/', views.add_media_to_favorite),
    path('favorite/', views.favorite_data),

	path('comment/create/', views.comment_create),

	path('media/<int:media_id>/like/add/', views.add_like),

	path('media/liked/list/', views.liked_media_list),

	path('media/liked/categorized/list/', views.categorized_liked_media),
		


]
