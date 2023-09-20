from django.urls import path
from. import consumers


print("routingggg")
websocket_urlpatterns=[
    path('machine_mqtt_data/', consumers.ChatConsumer.as_asgi()),
    path('kpi_web_socket/', consumers.KpiConsumer.as_asgi())

]




