from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
import re
from django.contrib.auth import authenticate
import random

class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    aadhar = forms.CharField(max_length=12)
    email = forms.EmailField()
    country_code = forms.CharField(max_length=5)
    mobile = forms.CharField(max_length=15)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address_line1 = forms.CharField(max_length=255)
    pincode = forms.CharField(max_length=6)
    district = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role', 'aadhar', 'email', 'country_code', 'mobile', 'first_name', 'last_name', 'address_line1', 'pincode', 'district', 'state', 'country']

    def clean_aadhar(self):
        aadhar = self.cleaned_data.get('aadhar')
        if not re.match(r'^\d{12}$', aadhar):
            raise forms.ValidationError('Aadhar number must be exactly 12 digits.')
        from .models import UserProfile
        if UserProfile.objects.filter(aadhar=aadhar).exists():
            raise forms.ValidationError('An account already exists with this Aadhar number.')
        return aadhar

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not re.match(r'^\d{10}$', mobile):
            raise forms.ValidationError('Mobile number must be exactly 10 digits.')
        from .models import UserProfile
        if UserProfile.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError('An account already exists with this mobile number.')
        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        from .models import UserProfile
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError('An account already exists with this email address.')
        return email

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not re.match(r'^\d{6}$', pincode):
            raise forms.ValidationError('Pincode must be exactly 6 digits.')
        return pincode

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        # Password constraints: 1 uppercase, 1 lowercase, 1 special, 1 digit
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password1):
            raise forms.ValidationError('Password must contain at least 1 uppercase, 1 lowercase, 1 special symbol, 1 digit, and be at least 8 characters long.')
        return password2

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        email = cleaned_data.get('email')
        mobile = cleaned_data.get('mobile')
        aadhar = cleaned_data.get('aadhar')
        from .models import UserProfile
        # Check for existing user by email, mobile, or aadhar
        for field, value in [('email', email), ('mobile', mobile), ('aadhar', aadhar)]:
            if value:
                existing = UserProfile.objects.filter(**{field: value}).first()
                if existing:
                    if existing.role != role:
                        if existing.role == 'seller' and role == 'buyer':
                            self.add_error(field, 'Already registered as a Seller')
                        elif existing.role == 'buyer' and role == 'seller':
                            self.add_error(field, 'Already registered as a Consumer')
                        else:
                            self.add_error(field, 'Already registered with this {}.'.format(field))
                    else:
                        self.add_error(field, 'Already registered with this {}.'.format(field))
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class MessageForm(forms.ModelForm):
    class Meta:
        model = UserProfile.Message if hasattr(UserProfile, 'Message') else None
        model = __import__('accounts.models', fromlist=['Message']).Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Type your message here...'}),
        }

class RatingForm(forms.ModelForm):
    score = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], label='Rating (1-5)')
    class Meta:
        model = __import__('accounts.models', fromlist=['Rating']).Rating
        fields = ['score', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional comment...'}),
        }

class CustomAuthForm(forms.Form):
    identifier = forms.CharField(label='Username / Email / Mobile / Aadhar')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('identifier')
        password = cleaned_data.get('password')
        from .models import UserProfile
        from django.contrib.auth.models import User
        user = None
        # Try to find user by username, email, mobile, or aadhar
        try:
            user_obj = User.objects.filter(username=identifier).first()
            if not user_obj:
                profile = UserProfile.objects.filter(email=identifier).first()
                if not profile:
                    profile = UserProfile.objects.filter(mobile=identifier).first()
                if not profile:
                    profile = UserProfile.objects.filter(aadhar=identifier).first()
                if profile:
                    user_obj = profile.user
            if user_obj:
                user = authenticate(username=user_obj.username, password=password)
        except Exception:
            user = None
        if not user:
            raise forms.ValidationError('Invalid credentials. Please try again.')
        self.user = user
        return cleaned_data

class ForgotPasswordForm(forms.Form):
    identifier = forms.CharField(label='Email / Mobile / Aadhar', max_length=150)

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=6)

class PasswordResetForm(forms.Form):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password1')
        p2 = cleaned_data.get('new_password2')
        if p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        # Password constraints: 1 uppercase, 1 lowercase, 1 special, 1 digit, min 8 chars
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', p1):
            raise forms.ValidationError('Password must contain at least 1 uppercase, 1 lowercase, 1 special symbol, 1 digit, and be at least 8 characters long.')
        return cleaned_data 