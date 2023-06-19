from django.urls import path
from. import consumers


print("routingggg")
websocket_urlpatterns=[
    path('machine_data', consumers.ChatConsumer.as_asgi())

]




