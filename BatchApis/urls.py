from django.urls import path, include
from .views import BatchViewSet, ForiegnFields
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'batchs', BatchViewSet, basename='batch')

urlpatterns = [
    path('', include(router.urls)),
    path('fetch/', ForiegnFields.as_view(), name='fetch'),
]