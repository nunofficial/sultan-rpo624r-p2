from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Ad, Review

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'city', 'image', 'title', 'description', 'price', 'vip_requested']
        widgets = {
            'image': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Вставьте ссылку на фото (URL)'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Опишите ваш товар...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена в тенге'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'vip_requested': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ваш отзыв...'}),
        }