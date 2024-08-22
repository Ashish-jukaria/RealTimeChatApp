from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import NameForm, SignupForm, LoginForm
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse








class Home(APIView):
    def get(self, request):
        return Response({'message':'Welcome to Home Page'})


class Register(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
    'refresh': str(refresh),
    'access': str(refresh.access_token),
})

class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):     
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)

class ChannelView(LoginRequiredMixin,View):
    login_url = '/login/'  # Redirects to this URL if the user is not logged in

    def get(self,request,channel_name):
        data=Group.objects.filter(group_name=channel_name).first()
        chat=[]
        if data:
            chat=Chat.objects.filter(group__group_name=channel_name).values_list('message', flat=True)
        else:
           group_create=Group(group_name=channel_name)
           group_create.save()

        # response_data = {
        #     'channel_name': channel_name,
        #     'chat': chat
        # }

        # return JsonResponse(response_data)

        return render(request,'myapp/channel.html',{'channel_name':channel_name,'chat':chat})

class UserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Assuming User model has fields like 'username', 'email', etc.
        return Response({
            'username': user.username,
            'email': user.email,
            # Add other user information as needed
        })

def get_group_names(request):
    # Retrieve all group names from the Group table
    group_names = Group.objects.values_list('group_name', flat=True)

    # Convert QuerySet to list and return as JSON response
    return JsonResponse(list(group_names), safe=False)
