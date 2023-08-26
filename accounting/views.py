from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounting.models import Expenses, Purchase, Balance
from accounting.serializers import ExpensesSerializer, PurchaseSerializer, BalanceSerializer


@api_view(['GET'])
def get_all_expenses(request):
    """
    Get all expenses.
    """
    expenses = Expenses.objects.all()
    serializer = ExpensesSerializer(expenses, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def get_all_purchase(request):
    """
    Get all purchase.
    """
    expenses = Purchase.objects.all()
    serializer = PurchaseSerializer(expenses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_balance(request):
    """
    Get all balance.
    """
    expenses = Balance.objects.all()
    serializer = BalanceSerializer(expenses, many=True)
    return Response(serializer.data)