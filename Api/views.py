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

