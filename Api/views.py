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