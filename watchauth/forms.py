from django import forms
from django.db import models
from froala_editor.fields import FroalaField
from .models import RepairRequest
  
class Page(models.Model):
    content = FroalaField()
    
    
    
class RepairRequestForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ['watch', 'customer', 'description'] 
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
   
    
    
    
    
