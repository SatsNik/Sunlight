from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, CustomAuthForm, ForgotPasswordForm, OTPVerificationForm, PasswordResetForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.core.mail import send_mail
import random
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

OTP_SESSION_KEY = 'registration_otp'
OTP_DATA_KEY = 'registration_data'

FORGOT_OTP_SESSION_KEY = 'forgot_otp'
FORGOT_USER_ID_SESSION_KEY = 'forgot_user_id'

# Registration view with OTP verification
def register_view(request):
    if request.method == 'POST':
        # If OTP is being submitted
        if 'otp' in request.POST:
            otp_input = request.POST.get('otp')
            otp_session = request.session.get(OTP_SESSION_KEY)
            form_data = request.session.get(OTP_DATA_KEY)
            if otp_input and otp_session and otp_input == otp_session:
                # OTP is correct, create user
                form = RegistrationForm(form_data)
                if form.is_valid():
                    user = form.save()
                    profile = UserProfile.objects.create(
                        user=user,
                        role=form.cleaned_data['role'],
                        aadhar=form.cleaned_data['aadhar'],
                        email=form.cleaned_data['email'],
                        country_code=form.cleaned_data['country_code'],
                        mobile=form.cleaned_data['mobile'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        address_line1=form.cleaned_data['address_line1'],
                        pincode=form.cleaned_data['pincode'],
                        district=form.cleaned_data['district'],
                        state=form.cleaned_data['state'],
                        country=form.cleaned_data['country'],
                    )
                    login(request, user)
                    messages.success(request, 'Registration successful!')
                    # Clear OTP session
                    request.session.pop(OTP_SESSION_KEY, None)
                    request.session.pop(OTP_DATA_KEY, None)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid registration data. Please try again.')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'accounts/register.html', {'form': RegistrationForm(request.session.get(OTP_DATA_KEY)), 'show_otp': True})
        # First step: registration form submission
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            # Send OTP via email
            email = form.cleaned_data['email']
            send_mail(
                'Your Sunlight Registration OTP',
                f'Your OTP for Sunlight registration is: {otp}',
                'noreply@sunlight.com',
                [email],
                fail_silently=True,
            )
            # Print OTP to console for SMS demo
            print(f"[SMS to {form.cleaned_data['mobile']}] Your Sunlight OTP is: {otp}")
            # Store OTP and form data in session
            request.session[OTP_SESSION_KEY] = otp
            request.session[OTP_DATA_KEY] = request.POST
            return render(request, 'accounts/register.html', {'form': form, 'show_otp': True})
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
    else:
        form = CustomAuthForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

# Forgot Password Step 1: Enter identifier
def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            user_obj = User.objects.filter(username=identifier).first()
            profile = None
            if not user_obj:
                profile = UserProfile.objects.filter(email=identifier).first()
                if not profile:
                    profile = UserProfile.objects.filter(mobile=identifier).first()
                if not profile:
                    profile = UserProfile.objects.filter(aadhar=identifier).first()
                if profile:
                    user_obj = profile.user
            else:
                profile = UserProfile.objects.filter(user=user_obj).first()
            if user_obj and profile:
                otp = str(random.randint(100000, 999999))
                # Send OTP via email
                send_mail(
                    'Your Sunlight Password Reset OTP',
                    f'Your OTP for Sunlight password reset is: {otp}',
                    'noreply@sunlight.com',
                    [profile.email],
                    fail_silently=True,
                )
                # Print OTP to console for SMS demo
                print(f"[SMS to {profile.mobile}] Your Sunlight password reset OTP is: {otp}")
                request.session[FORGOT_OTP_SESSION_KEY] = otp
                request.session[FORGOT_USER_ID_SESSION_KEY] = user_obj.id
                return redirect('verify_forgot_otp')
            else:
                messages.error(request, 'No user found with that identifier.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})

# Forgot Password Step 2: Verify OTP
def verify_forgot_otp_view(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        otp_session = request.session.get(FORGOT_OTP_SESSION_KEY)
        if form.is_valid():
            otp_input = form.cleaned_data['otp']
            if otp_input == otp_session:
                return redirect('reset_password')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    return render(request, 'accounts/verify_forgot_otp.html', {'form': form})

# Forgot Password Step 3: Reset Password
from django.contrib.auth.hashers import make_password

def reset_password_view(request):
    user_id = request.session.get(FORGOT_USER_ID_SESSION_KEY)
    if not user_id:
        messages.error(request, 'Session expired. Please try again.')
        return redirect('forgot_password')
    user = User.objects.filter(id=user_id).first()
    if not user:
        messages.error(request, 'User not found.')
        return redirect('forgot_password')
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.password = make_password(new_password)
            user.save()
            # Clear session
            request.session.pop(FORGOT_OTP_SESSION_KEY, None)
            request.session.pop(FORGOT_USER_ID_SESSION_KEY, None)
            messages.success(request, 'Password reset successful! You can now log in.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/reset_password.html', {'form': form})


@login_required
@require_POST
def update_address(request):
    try:
        data = json.loads(request.body)
        profile = request.user.profile
        
        profile.address_line1 = data.get('address_line1', '')
        profile.district_state = data.get('district_state', '')
        profile.country = data.get('country', '')
        profile.pincode = data.get('pincode', '')
        
        profile.save()
        return JsonResponse({'message': 'Address updated successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)