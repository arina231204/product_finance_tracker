from django.urls import path
from .views import contractor_list, contractor_detail, product_list, product_detail, receipt_list, receipt_detail, cancellation_list, cancellation_detail, inventory_detail, inventory_list

urlpatterns = [
    path('contractors/', contractor_list, name='contractor_list'),
    path('products/', product_list, name='product_list'),
    path('contractors/<int:pk>/', contractor_detail, name='contractor_detail'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('receipts/', receipt_list),
    path('receipts/<int:pk>/', receipt_detail),
    path('cancellation/', cancellation_list ),
    path('cancellation/<int:pk>/', cancellation_detail),
    path('inventory/', inventory_list ),
    path('inventory/<int:pk>/', inventory_detail),
]
