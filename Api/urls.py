from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.user_register),
    path('login/', views.user_login),
	path('user/', views.user_data),
	path('profile/edit/', views.profile_edit),

	path('artist/', views.artist_data),
	path('artist/edit/', views.artist_edit),
	path('user/unfollow/', views.user_unfollow),
	path('media/categorized/list/', views.categorized_media),
	path('media/create/', views.media_create),
	path('user/followed/list/', views.followed_users_list),
	path('favorite/create/', views.favorite_create),
	path('post/create/', views.post_create),

]
