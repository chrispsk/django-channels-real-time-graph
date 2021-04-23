import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from django.urls import path
from .consumers import WSConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setari.settings')

ws_urlpatterns = [
    path('ws/some_url/', WSConsumer.as_asgi()),
]

# first, django channels checks the type of the connection (the protocol type): http or websocket
# if the con is the websocket connection it will be given to the AuthMiddlewareStack to identify a user.
# I don't use users here so will be Anonymous lazy user object
# After that the connection will be given to the URLRouter class that pass it to the consumer defined in ws_urlpatterns
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns))
})