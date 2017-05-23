from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        # Indicating model to use to dynamically create a form
        model = Comment

        # Explicitely defining the fields needed
        fields = ('name', 'email', 'body')