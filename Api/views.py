from itertools import chain

from django.contrib.auth import authenticate
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer, ArtistSerializer, MediaSerializer, FavoriteSerializer, CommentSerializer
from .models import CustomUser, Artist, Media, Favorite, Following


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user and user.is_active:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'data': 'logged in successfully',
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=status.HTTP_200_OK)
    return Response({'data': 'invalid Username or Password!'}, status=status.HTTP_400_BAD_REQUEST)


	
@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    user = CustomUser.objects.filter(username=request.POST.get('username'))
    if user.exists():
        return Response({'data': 'Username already exists!'}, status=status.HTTP_400_BAD_REQUEST)
    if request.POST.get('password') == request.POST.get('re_password'):
        try:
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                new_user = user_serializer.save()
                token, created = Token.objects.get_or_create(user=new_user)
                new_user.save()
                return Response({
                    'data': 'registered successfully.',
                    'token': token.key,
                    'user_id': new_user.pk,
                    'artist_id': new_user.artist.pk if hasattr(new_user, 'artist') else "",
                    'email': new_user.email
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'data': 'Passwords not match!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_data(request):
    try:
        user = CustomUser.objects.get(pk=request.user.id)
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)
    except:
        return Response({'data': 'user does not exits!'}, status=status.HTTP_404_NOT_FOUND)


		
@api_view(['PUT'])
def profile_edit(request):
    serialized_artist = UserSerializer(request.user, data=request.data, partial=True)
    if serialized_artist.is_valid():
        serialized_artist.save()
        return Response(serialized_artist.data, status=status.HTTP_200_OK)
    return Response({'data': 'invalid data'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def artist_data(request):
    if not hasattr(request.user, 'artist'):
        return Response({'data': 'You dont have access!'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        artist = Artist.objects.get(pk=request.user.artist.id)
        serialized_artist = ArtistSerializer(artist)
        return Response(serialized_artist.data, status=status.HTTP_200_OK)
    except:
        return Response({'data': 'artist does not exits!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def artist_profile_data(request, artist_id):
    try:
        artist = Artist.objects.get(pk=artist_id)
        following = Following.objects.get(user_id=artist.user.id)
        _users = following.followed.all().count()
        follower_users = following.follower.all().count()
        album_count = Album.objects.filter(artist=artist).count()
        music_count = Media.objects.filter(type=1, artist=artist).count()
        serialized_artist = ArtistSerializer(artist)

        result = {'follower_users': follower_users, 'followed_users': followed_users,
                  'album_count': album_count, 'music_count': music_count, **serialized_artist.data}
        return Response(result, status=status.HTTP_200_OK)
    except:
        return Response({'data': 'artist does not exits!'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
def artist_edit(request):
    if not hasattr(request.user, 'artist'):
        return Response({'data': 'You dont have access!'}, status=status.HTTP_400_BAD_REQUEST)
    artist = Artist.objects.filter(pk=request.user.artist.id)
    if artist.exists():
        artist = artist.first()
        serialized_artist = ArtistSerializer(artist, data=request.data, partial=True)
        if serialized_artist.is_valid():
            serialized_artist.save()
            return Response(serialized_artist.data, status=status.HTTP_200_OK)
    return Response({'data': 'artist does not exits!'}, status=status.HTTP_404_NOT_FOUND)


@@api_view(['GET'])
def search(request):
    media_lookup = Q()
    artist_lookup = Q()
    user_lookup = Q()
    search_type = request.GET.get('searchType', 'media')
    if search_type == 'media':
        if title := request.GET.get('title', ''):
            media_lookup &= Q(title__contains=title)
        if media_type := request.GET.get('type', ''):
            media_lookup &= Q(type=media_type)
        if genre := request.GET.get('genre', ''):
            media_lookup &= Q(genre=genre)
        if username := request.GET.get('username', ''):
            media_lookup &= Q(artist__user__username__contains=username)
        if first_name := request.GET.get('first_name', ''):
            media_lookup &= Q(artist__user__first_name__contains=first_name)
        if last_name := request.GET.get('last_name', ''):
            media_lookup &= Q(artist__user__last_name__contains=last_name)
        medias = MediaSerializer(Media.objects.filter(media_lookup), many=True).data
        return Response(medias, status=status.HTTP_200_OK)
    elif search_type == 'artist':
        if genre := request.GET.get('genre', ''):
            artist_lookup &= Q(genre=genre)
        if username := request.GET.get('username', ''):
            artist_lookup &= Q(user__username__contains=username)
        if first_name := request.GET.get('first_name', ''):
            artist_lookup &= Q(user__first_name__contains=first_name)
        if last_name := request.GET.get('last_name', ''):
            artist_lookup &= Q(user__last_name__contains=last_name)
        artists = ArtistSerializer(Artist.objects.filter(artist_lookup), many=True).data
        return Response(artists, status=status.HTTP_200_OK)
    elif search_type == 'user':
        if username := request.GET.get('username', ''):
            user_lookup &= Q(username__contains=username)
        if first_name := request.GET.get('first_name', ''):
            user_lookup &= Q(first_name__contains=first_name)
        if last_name := request.GET.get('last_name', ''):
            user_lookup &= Q(last_name__contains=last_name)
        users = UserSerializer(CustomUser.objects.filter(user_lookup), many=True).data
        return Response(users, status=status.HTTP_200_OK)
    return Response({'data': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['GET'])
def liked_media_list(request):
    try:
        medias = Media.objects.filter(likes__isnull=False)
        serialized_medias = MediaSerializer(medias, many=True)
        return Response(serialized_medias.data, status=status.HTTP_200_OK)
    except:
        return Response({'data': 'liked media does not exits!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def categorized_liked_media(request):
    try:
        medias = Media.objects.filter(type=request.GET.get('type', 1), likes__isnull=False)
        serialized_medias = MediaSerializer(medias, many=True)
        return Response(serialized_medias.data, status=status.HTTP_200_OK)
    except:
        return Response({'data': 'categorized media does not exits!'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def favorite_create(request):
    try:
        user_id = request.user.id
        request.data._mutable = True
        request.data['user'] = user_id
        request.data._mutable = False
        serialized_favorite = FavoriteSerializer(data=request.data)
        if serialized_favorite.is_valid():
            serialized_favorite.save()
        return Response(serialized_favorite.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_media_to_favorite(request, favorite_id):
    media_id = request.POST.get('media')

    favorite = Favorite.objects.filter(pk=favorite_id)
    if favorite.exists():
        favorite = favorite.first()
        favorite.medias.add(media_id)
        return Response({'data': 'the favorite data updated successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'data': 'favorite does not exits!'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def favorite_data(request):
    try:
        favorite = Favorite.objects.filter(user_id=request.user.id)
        serialized_favorite = FavoriteSerializer(favorite, many=True)
        return Response(serialized_favorite.data, status=status.HTTP_200_OK)
    except:
        return Response({'data': 'favorite does not exits!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def favorite_medias_list(request, favorite_id):
    try:
        favorite = Favorite.objects.get(id=favorite_id)
        medias = favorite.medias.all()
        serialized_media = MediaSerializer(medias, many=True)
        return Response(serialized_media.data, status=status.HTTP_200_OK)
    except:
        return Response({'data': 'favorite does not exits!'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def comment_create(request):
    try:
        user_id = request.user.id
        request.data._mutable = True
        request.data['user'] = user_id
        request.data._mutable = False
        serialized_comment = CommentSerializer(data=request.data)
        if serialized_comment.is_valid():
            serialized_comment.save()
        return Response(serialized_comment.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_like(request, media_id):
    media = Media.objects.filter(pk=media_id)
    if media.exists():
        media = media.first()
        media.likes.add(request.user)
        return Response({'data': 'the media data updated successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'data': 'media does not exits!'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def post_create(request):
    try:
        user_id = request.user.id
        request.data._mutable = True
        request.data['user'] = user_id
        request.data._mutable = False
        serialized_post = PostSerializer(data=request.data)
        if serialized_post.is_valid():
            serialized_post.save()
        return Response(serialized_post.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_posts_list(request, user_id):
    try:
        posts = Post.objects.filter(user_id=user_id)
        serialized_post = PostSerializer(posts, many=True)
        return Response(serialized_post.data, status=status.HTTP_200_OK)
    except:
        return Response({'data': 'posts does not exits!'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def categorized_media(request):
    try:
        medias = Media.objects.filter(type=request.GET.get('type', 1))
        serialized_medias = MediaSerializer(medias, many=True)
        return Response(serialized_medias.data, status=status.HTTP_200_OK)
    except:
        return Response({'data': 'categorized media does not exits!'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def media_create(request):
    if not hasattr(request.user, 'artist'):
        return Response({'data': 'You dont have access!'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        artist_id = request.user.artist.id
        request.data._mutable = True
        request.data['artist'] = artist_id
        request.data._mutable = False
        serialized_media = MediaSerializer(data=request.data)
        if serialized_media.is_valid():
            serialized_media.save()
            return Response(serialized_media.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def music_newest_list(request):
    try:
        musics = Media.objects.filter(type=1).order_by('-create_datetime')
        serialized_musics = MediaSerializer(musics, many=True)
        return Response(serialized_musics.data, status=status.HTTP_200_OK)
    except:
        return Response({'data': 'musics does not exits!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def user_follow(request):
    try:
        user_id = request.POST.get('user_id')
        follow_user = CustomUser.objects.get(id=user_id)
        Following.follow(user=request.user, another_account=follow_user)
        return Response({'data': 'followed successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_unfollow(request):
    try:
        user_id = request.POST.get('user_id')
        unfollow_user = CustomUser.objects.get(id=user_id)
        Following.unfollow(user=request.user, another_account=unfollow_user)
        return Response({'data': 'unfollowed successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def followed_users_list(request):
    try:
        following = Following.objects.get(user_id=request.user.id)
        followed_users = following.followed.all()
        serialized_users = UserSerializer(followed_users, many=True)
        return Response(serialized_users.data, status=status.HTTP_200_OK)
    except:
        return Response({'data': 'following does not exits!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def album_create(request):
    try:
        serialized_album = AlbumSerializer(data=request.data)
        if serialized_album.is_valid():
            serialized_album.save()
            return Response(serialized_album.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def album_data(request, album_id):
    try:
        album = Album.objects.get(pk=album_id)
        serialized_album = AlbumSerializer(album)
        return Response(serialized_album.data, status=status.HTTP_200_OK)
    except:
        return Response({'data': 'album does not exits!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def album_most_seen_list(request):
    try:
        albums = Album.objects.all().order_by('-seen')
        serialized_albums = MediaSerializer(albums, many=True)
        return Response(serialized_albums.data, status=status.HTTP_200_OK)
    except:
        return Response({'data': 'albums does not exits!'}, status=status.HTTP_404_NOT_FOUND)
