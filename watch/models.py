from django import forms
from django.db import models



# Create your models here.

class Cat(models.Model):
    watch_type = models.CharField(max_length=1000, blank=True, null=True)
    type_detail = models.TextField
    def __str__(self):
        return self.watch_type
    
class Product(models.Model):
    product_id = models.AutoField
    
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    # category = models.ForeignKey(Cat, on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    feature_vector = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.product_name
   
class FeatureVector(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    feature_vector = models.TextField()

    def __str__(self):
        return str(self.product)
    
    
# class SearchForm(forms.Form):
#     query = forms.CharField(max_length=100)  






