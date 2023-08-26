from rest_framework import serializers
from .models import Test, Products

class TestSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()

    def create(self, validate_data):

        return Test.objects.create(**validate_data)

    def update(self, instance, validate_data):

        instance.name = validate_data.get('name', instance.name)
        instance.age = validate_data.get('age', instance.age)
        instance.save()
        return instance


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    group = serializers.CharField()
    country = serializers.CharField()
    provider = serializers.CharField()
    articul = serializers.CharField()
    code = serializers.CharField()
    amount = serializers.IntegerField()
    price = serializers.IntegerField()
    status = serializers.IntegerField()

    def create(self, validate_data):

        return Products.objects.create(**validate_data)