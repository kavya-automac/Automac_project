from django.urls import path
from. import consumers


print("routingggg")
websocket_urlpatterns=[
    path('ws/ac/', consumers.MyAsyncConsumer.as_asgi()),

]