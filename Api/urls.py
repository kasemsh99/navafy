from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.user_register),
    path('login/', views.user_login),
	path('user/', views.user_data),
	path('profile/edit/', views.profile_edit),

	path('artist/', views.artist_data),
	path('artist/<int:artist_id>/profie/', views.artist_profile_data),
	path('artist/edit/', views.artist_edit),

	path('search/', views.search),

	path('media/<int:media_id>/like/add/', views.add_like),
	path('media/liked/categorized/list/', views.categorized_liked_media),
	
	path('media/categorized/list/', views.categorized_media),
	path('favorite/create/', views.favorite_create),
	path('favorite/<int:favorite_id>/media/add/', views.add_media_to_favorite),
	path('favorite/', views.favorite_data),
	path('favorite/<int:favorite_id>/media/list/', views.favorite_medias_list),
	path('user/follow/', views.user_follow),
	path('comment/create/', views.comment_create),
	path('media/<int:media_id>/like/add/', views.add_like),
	
	path('post/create/', views.post_create),
	path('user/<int:user_id>/post/list/', views.user_posts_list),
	path('media/create/', views.media_create),
	path('user/unfollow/', views.user_unfollow),
	path('user/followed/list/', views.followed_users_list),
	path('music/newest/list/', views.music_newest_list),
	path('music/most-seen/list/', views.music_most_seen_list),
	path('music/by-genre/list/', views.music_by_genre_list),
]
