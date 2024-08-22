from django.urls import path
from . import consumers

websocket_urlpatterns=[
    path('ws/sc/<str:groupname>/',consumers.FirstConsumer.as_asgi())
]