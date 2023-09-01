from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from .models import Item, Review, Address, Payment

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'firstname', 'lastname', 'email', 'password1', 'password2')
        
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'form-control rounded-pill',
    }))
    
    firstname = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your first name',
        'class': 'form-control rounded-pill',
    }))
    
    lastname = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your last name',
        'class': 'form-control rounded-pill',
    }))
    
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email',
        'class': 'form-control rounded-pill',
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'form-control rounded-pill',
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your passowrd',
        'class': 'form-control rounded-pill',
    }))

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class' : 'form-control rounded-pill',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class' : 'form-control rounded-pill',
    }))
    
    
INPUT_CLASSES = 'form-control'
class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image')
        widgets= {
            'category' : forms.Select(attrs={
                'class' : INPUT_CLASSES
            }),
            'name' : forms.TextInput(attrs={
                'class' : INPUT_CLASSES
            }),
            'description' : forms.Textarea(attrs={
                'class' : INPUT_CLASSES
            }),
            'price' : forms.TextInput(attrs={
                'class' : INPUT_CLASSES
            }),
            'image' : forms.FileInput(attrs={
                'class' : INPUT_CLASSES
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label = 'Category'
        self.fields['name'].label = 'Name'
        self.fields['description'].label = 'Description'
        self.fields['price'].label = 'Price'
        self.fields['image'].label = 'Image'
        self.fields['image'].required = True
        
class ItemSearch(forms.ModelForm):
    query = forms.CharField(label='Search', max_length=100,widget=forms.TextInput(attrs={
        'class' : 'form-control rounded-pill',
    }))

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=99)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

INPUT_CLASSES = 'form-control'
class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image')
        widgets= {
            'category' : forms.Select(attrs={
                'class' : INPUT_CLASSES
            }),
            'name' : forms.TextInput(attrs={
                'class' : INPUT_CLASSES
            }),
            'description' : forms.Textarea(attrs={
                'class' : INPUT_CLASSES
            }),
            'price' : forms.TextInput(attrs={
                'class' : INPUT_CLASSES
            }),
            'image' : forms.FileInput(attrs={
                'class' : INPUT_CLASSES
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label = 'Category'
        self.fields['name'].label = 'Name'
        self.fields['description'].label = 'Description'
        self.fields['price'].label = 'Price'
        self.fields['image'].label = 'Image'
        self.fields['image'].required = True

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address', 'address2', 'country', 'state', 'zip')
        widgets= {
            'address' : forms.TextInput(attrs={
                'class' : INPUT_CLASSES
            }),
            'address2' : forms.TextInput(attrs={
                'class' : INPUT_CLASSES
            }),
            'country' : forms.TextInput(attrs={
                'class' : INPUT_CLASSES
            }),
            'state' : forms.TextInput(attrs={
                'class' : INPUT_CLASSES
            }),
            'zip' : forms.TextInput(attrs={
                'class' : INPUT_CLASSES
            }),
        }
        
class PaymentForm(forms.ModelForm):
    METHOD_CHOICES = (
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Paypal Card', 'Paypal Card'),
    )
    
    method = forms.ChoiceField(choices=METHOD_CHOICES, widget=forms.Select(attrs={
        'class': INPUT_CLASSES
    }))
    
    class Meta:
        model = Payment
        fields = ('method', 'name', 'cardnumber', 'expire_month', 'expire_year', 'cvv')
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'cardnumber': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'expire_month': forms.Select(attrs={'class': INPUT_CLASSES}),
            'expire_year': forms.Select(attrs={'class': INPUT_CLASSES}),
            'cvv': forms.TextInput(attrs={'class': INPUT_CLASSES}),
        }

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'step': '0.5',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '2',
            }),
        }