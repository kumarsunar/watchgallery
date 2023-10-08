from django.db import models

class Watchauth(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    # Add any other fields you need

class RepairRequest(models.Model):
    watch = models.ForeignKey(Watchauth, on_delete=models.CASCADE)
    customer = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Add any other fields you need

from django.contrib.auth.models import User


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    # other fields...




