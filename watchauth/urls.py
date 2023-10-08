
# from django.urls import path
# from watchauth import views

from django.urls import path
from watchauth import views
from .views import  RepairRequestCreateView

app_name = "watchauth"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.handlelogin, name='handlelogin'),
    path('logout/', views.handlelogout, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('about/', views.about, name="about"),
    path('repair_request/', RepairRequestCreateView.as_view(), name='repair_request'),
    
    path('search/', views.search, name='product_search'),
    
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(), name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(), name='set-new-password'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),    
   
]
