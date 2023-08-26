from django.urls import path
from . import views as v_accounting
urlpatterns = [
    path('expenses/', v_accounting.get_all_expenses),
    path('purchase/', v_accounting.get_all_purchase),
    path('balance/', v_accounting.get_all_balance),



]
