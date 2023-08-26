from django.urls import path

from .views import store, store_detail, products

urlpatterns = [
    path('store/', store),
    path('store/<int:pk>/', store_detail),
    path('products/', products),
]

