# -*- coding:UTF-8 -*-

from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .exceptions import ProfileDoesNotExist
from .models import Profile
from .serializers import ProfileSerializer
from .renderers import ProfileJSONRenderer

class ProfileRetrieveAPIView(RetrieveAPIView):
    queryset = Profile.objects.select_related('user')
    permission_classes = (AllowAny,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer 

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        serializer = self.serializer_class(profile, context={
            'request':request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileFollowAPIView(APIView): 
    queryset = Profile.objects.select_related('user')
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer 
    
    def delete(self, request, username=None):
        follower = self.request.user.profile
        
        try:
            followee = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        follower.unfollow(followee)

        serializer = self.serializer_class(followee, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, username=None):
        follower = self.request.user.profile
        
        try:
            followee = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        if followee.pk is follower.pk:
            raise serializers.ValidationError('You can not follow yourself')

        follower.follow(followee)

        serializer = self.serializer_class(followee, context={
            'request': request 
        })

        return Response(serializer.data, status=status.HTTP_200_OK)
