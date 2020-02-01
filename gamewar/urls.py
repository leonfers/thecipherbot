from django.urls import path, include
from rest_framework import routers

from game import views

router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewset)
router.register(r'telegram', views.TelegramUpdate, basename="telegram")

urlpatterns = [
    path('', include(router.urls)),
]
