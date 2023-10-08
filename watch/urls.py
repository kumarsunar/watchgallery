
from django.urls import include, path
from watch import views


app_name = "watch"


urlpatterns = [
    path('',views.home,name='home'),
    path("products/<int:pk>/", views.product_detail, name="productdetail"),
   
]    
   
