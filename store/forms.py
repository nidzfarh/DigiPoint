from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Order, Product


def validate_indian_pincode(value):
    """Validate Indian PIN code format (6 digits)."""
    if not value.isdigit() or len(value) != 6:
        raise ValidationError('PIN code must be exactly 6 digits.')


def validate_indian_phone(value):
    """Validate Indian phone number format (+91 prefix optional, 10 digits)."""
    phone = value.replace('-', '').replace(' ', '').replace('+', '')
    
    if phone.startswith('91'):
        if len(phone) != 12 or not phone.isdigit():
            raise ValidationError('Phone number must be in format: +91-9876543210 or 9876543210')
    else:
        if len(phone) != 10 or not phone.isdigit():
            raise ValidationError('Phone number must be 10 digits starting with 6-9.')


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class OrderForm(forms.ModelForm):
    """Form for creating orders with Indian address format."""
    
    class Meta:
        model = Order
        fields = ('shipping_address', 'shipping_city', 'shipping_state', 
                  'shipping_postal_code', 'shipping_country', 'phone_number')
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'House/Flat No., Street Address',
                'rows': 3
            }),
            'shipping_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City (e.g., Bengaluru, Mumbai, Delhi)'
            }),
            'shipping_state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State (e.g., Karnataka, Maharashtra)'
            }),
            'shipping_postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'PIN Code (6 digits)',
                'maxlength': '6'
            }),
            'shipping_country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country',
                'value': 'India',
                'readonly': 'readonly'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91-9876543210 or 9876543210'
            }),
        }
    
    def clean_shipping_postal_code(self):
        """Validate PIN code."""
        pin_code = self.cleaned_data.get('shipping_postal_code')
        if pin_code:
            validate_indian_pincode(pin_code)
        return pin_code
    
    def clean_phone_number(self):
        """Validate phone number."""
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            validate_indian_phone(phone_number)
        return phone_number


class ProductSearchForm(forms.Form):
    """Form for product search."""
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search products...'
        })
    )
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + list(Product._meta.get_field('category').choices),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


class CartQuantityForm(forms.Form):
    """Form for updating cart item quantity."""
    quantity = forms.IntegerField(
        min_value=1,
        max_value=999,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 80px;'
        })
    )
