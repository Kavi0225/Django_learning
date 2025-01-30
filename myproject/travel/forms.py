from django import forms
from .models import Comments

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']