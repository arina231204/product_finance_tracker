from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()

class Equipments(models.Model):
    pass

class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    group = models.CharField(max_length=50)
    country = models.CharField(max_length=60)
    provider = models.CharField(max_length=60)
    articul = models.CharField(max_length=60)
    code = models.CharField(max_length=60)
    amount = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    status = models.PositiveSmallIntegerField(default=0)

