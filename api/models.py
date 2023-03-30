from django.db import models
from simple_history.models import HistoricalRecords

class Product(models.Model):
    pid=models.CharField(max_length=20,default=None,unique=True)
    name=models.CharField(max_length=200,default=None)
    price=models.FloatField(default=0.0)
    product_slug=models.SlugField(default="",blank=True,max_length=300, allow_unicode=True)
    product_image=models.TextField(default=None)
    active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True, null=True, blank=True)

class Tickets(models.Model):
    key = models.CharField(max_length=100,default=None,unique=True)
    title = models.CharField(max_length=200,default=None)
    project_name = models.CharField(max_length=100,default=None)
    priority= models.CharField(max_length=10,default=None)
    updated_date = models.DateField(auto_now_add=False, null=True, blank=True)
    ticket_status = models.CharField(max_length=20,default=None)
    creator_email = models.CharField(max_length=50,default=None)
    created_date = models.DateField(auto_now_add=False, null=True, blank=True)