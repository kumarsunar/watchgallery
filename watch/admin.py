from django.contrib import admin
from watch.models import Product
from django_summernote.admin import SummernoteModelAdmin



class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ('desc')
    
    
    class meta:
        model = Product


# Register your models here.
admin.site.register(Product,ProductAdmin)


