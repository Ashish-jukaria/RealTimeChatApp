from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('', Home.as_view(), name="home"),  # Home view
    path('register/', Register.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', logout, name='logout'),
    path('channel/<str:channel_name>/',ChannelView.as_view(),name='cahnnel_view'),
    path('user-info/', UserInfo.as_view(), name='user-info'),

    path('token/', 
          jwt_views.TokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
     path('token/refresh/', 
          jwt_views.TokenRefreshView.as_view(), 
          name ='token_refresh'),

     path('groups/', get_group_names, name='get_group_names'),

     

    


]

