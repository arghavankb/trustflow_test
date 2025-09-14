from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet
from django.urls import path, include


router = DefaultRouter()
router.register("transactions", TransactionViewSet, basename="transactions")

urlpatterns = [
    path('', include(router.urls)),
]
