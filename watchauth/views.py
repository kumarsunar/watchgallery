
from email.message import EmailMessage
from tokenize import generate_tokens
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.generic.base import View
from django.utils.encoding import DjangoUnicodeDecodeError
from django.views.generic.edit import FormView
from django.urls import reverse_lazy


#to activate user account
from django.urls import reverse ,reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from requests import request
from stripe import Product

from watchauth.forms import RepairRequestForm


from.utils import TokemGenerator, generate_token

#email

from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
from django.conf import settings

#threading
import threading

#reset password generators

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model

from payment.models import Cart



class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message=email_message
        
    def run(self):
        self.email_message.send()    




# Create your views here.


from django.core.mail import EmailMessage
from django.conf import settings

# def signup(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('pass1')
#         confirm_password = request.POST.get('pass2')
        
#         if password != confirm_password:
#             messages.warning(request, "Passwords do not match")
#             return render(request, 'auth/signup.html')
        
#         try:
#             if User.objects.get(username=email):
#                 messages.warning(request, "Email is already taken")
#                 return render(request, 'auth/signup.html')
#         except user.DoesNotExist:
#             pass
        
#         user = user.objects.create_user(username=email, email=email, password=password)
#         user.is_active = True
#         user.save()
        
#         current_site = get_current_site(request)
#         email_subject = "Activate Your Account"
#         message = render_to_string('auth/activate.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': generate_token.make_token(user)
#         })
        
#         email_message = EmailMessage(
#             email_subject, 
#             message, 
#             settings.DEFAULT_FROM_EMAIL, 
#             [email],
#             reply_to=[settings.DEFAULT_FROM_EMAIL]
#         )
#         email_message.content_subtype = "html" # set the content type of the email
        
        
#         messages.info(request, "Activate your account by clicking on the link in your email")
#         return redirect('handlelogin')
    
#     return render(request, 'auth/signup.html')


User = get_user_model()

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        confirm_password = request.POST.get('pass2')
        
        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
            return render(request, 'auth/signup.html')
        
        try:
            if User.objects.get(username=email):
                messages.warning(request, "Email is already taken")
                return render(request, 'auth/signup.html')
        except User.DoesNotExist:
            pass
        
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False
        user.save()
        
        current_site = get_current_site(request)
        email_subject = "Activate Your Account"
        message = render_to_string('auth/activate.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        
        email_message = EmailMessage(
            email_subject, 
            message, 
            settings.DEFAULT_FROM_EMAIL, 
            [email],
            reply_to=[settings.DEFAULT_FROM_EMAIL]
        )
        email_message.content_subtype = "html"  # set the content type of the email
        
        email_message.send()
        
        messages.info(request, "Activate your account by clicking on the link in your email")
        return redirect('watchauth:handlelogin')
    
    return render(request, 'auth/signup.html')





class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Account Activated Successfully")
            return redirect('handlelogin')
        return render(request, 'auth/login.html')

    









def handlelogin(request):
    if request.method=="POST":

        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            # return render(request,'index.html')
            return redirect('watch:home')
    
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/watchauth/login')

    return render(request,'auth/login.html')   



def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return redirect('watchauth:handlelogin')
    




# class RequestResetEmailView(View):
#     def get(self,request):
#         return render(request,'auth/request-reset-email.html')
#     # template_name = 'auth/request-reset-email.html'
    
#     def post(self,request):
#         email=request.POST['email']
#         user =User.objects.filter(email=email)
        
#         if user.exits():
#             current_site=get_current_site(request)
#             email_subject='[Reset Your Password]'
#             messages=render_to_string('auth/reset-user-password.html',
#             {
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
#                 'token': PasswordResetTokenGenerator().make_token(user[0])
                
#             })
            
#             email_message=EmailMessage(email_subject,messages,settings.
#                                        EMAIL_HOST_USER,[email])
#             EmailThread(email_message).start()
            
#             messages.info(request,"WE HAVE SENT YOU AN EMAIL WITH INSTRUCTIONS ON HOW TO RESET THE PASSWORD")
#             return render(request,'auth/request-reset-email.html')
        
        
        
        
class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'auth/request-reset-email.html')

    def post(self, request):
        email = request.POST['email']
        user = User.objects.filter(email=email)
        
        print("User: ", user) # add this print statement
        
        if user.exists():
            current_site = get_current_site(request)
            email_subject = '[Reset Your Password]'
            message = render_to_string('auth/reset-user-password.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            })
            
            email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
            EmailThread(email_message).start()
            email_message.send()
            
            messages.info(request, "WE HAVE SENT YOU AN EMAIL WITH INSTRUCTIONS ON HOW TO RESET YOUR PASSWORD")
            return HttpResponseRedirect('/watchauth/login/')
        
        messages.error(request, "THERE IS NO ACCOUNT ASSOCIATED WITH THIS EMAIL ADDRESS")
        return render(request, 'auth/request-reset-email.html')


class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link is Invalid")
                return render(request,'/auth/request-reset-email.html')
            
        except DjangoUnicodeDecodeError as identifier:
            pass
        
        return render(request,'/auth/set-new-password.html',context)
    
    
    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password = request.POST.get('pass1')
        confirm_password = request.POST.get('pass2')
        
        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
            return render(request, 'auth/set-new-password.html',context)
        
        try:
            user_id= str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Success Please Login With NewPassword")
            return redirect('/watchauth/login/')
        
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something Went Wrong")
            return render(request,'auth/set-new-password.html',context)
        
def checkout(request):
    cart = Cart.objects.get(user=request.user)  # Assuming the current user's cart is retrieved using the user attribute
    products = cart.products.all()  # Retrieve all products associated with the cart
    
    context = {
        'products': products
    }
    
    return render(request, 'checkout.html', context) 



def about(request):
    return render(request, "about.html")





class RepairRequestCreateView(FormView):
    template_name = 'repair_request.html'
    form_class = RepairRequestForm
    success_url = reverse_lazy('/about')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    
    
from django.views.generic import TemplateView

class RepairRequestView(TemplateView):
    template_name = 'repair_request.html'
    
    
from django.shortcuts import render
from watch.models import Product

def search(request):
    query = request.GET.get('query')
    print(query)
    products = []

    if query:
        # Perform a case-insensitive search on the 'name' field
        products = Product.objects.filter(product_name__icontains=query)
        print("Search Query:", query)
        print("Products Found:", products)

    return render(request, 'product_search.html', {'products': products, 'query': query})



 
from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment
from .forms import CommentForm

from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentForm

def post_detail(request):
    comments = Comment.objects.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect('post_detail')
    else:
        form = CommentForm()

    return render(request, 'index.html', {'comments': comments, 'form': form})























