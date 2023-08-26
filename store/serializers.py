from rest_framework import serializers
from .models import Contractor, Product, Receipt, Сancellation, Inventory, Country, Department, NDS, Group, Warehouse, \
    Project, Contact, BankCode, UnitOfMeasurement, EGAISCode, AccountingFeatures


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'

class CancellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Сancellation
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class NDSSerializer(serializers.ModelSerializer):
    class Meta:
        model = NDS
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class BankCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCode
        fields = '__all__'


class UnitOfMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasurement
        fields = '__all__'

class EGAISCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EGAISCode
        fields = '__all__'

class AccountingFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountingFeatures
        fields = '__all__'