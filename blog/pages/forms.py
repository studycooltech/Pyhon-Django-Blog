from django import forms
from django.forms import TextInput, Textarea, SelectDateWidget, Select
from .models import Post,Profile



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug' ,'category', 'content', 'published', 'image']

        widgets = {
            'title': TextInput(attrs={'class':'form-control'}),
            'slug': TextInput(attrs={'class':'form-control'}),
            'category': Select(attrs={'class':'form-control'}),
            'published': SelectDateWidget(attrs={'class':'form-control'}),
            'content': Textarea(attrs={'class':'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', ]

        widgets = {
            'profile_name': TextInput(attrs={'class':'form-control'}),
            'email': TextInput(attrs={'class':'form-control'}),
            'address': TextInput(attrs={'class':'form-control'}),
        }
