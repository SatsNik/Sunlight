from django.shortcuts import render, redirect
from accounts.models import UserProfile, Wallet
from django.contrib.auth.decorators import login_required
from accounts.forms import MessageForm, RatingForm
from accounts.models import Message, Rating
from django.db.models import Avg
from django.contrib import messages
import json
from decouple import config
# Create your views here.

@login_required
def dashboard_view(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.role == 'buyer':
        return redirect('buyer_dashboard')
    elif profile.role == 'seller':
        return redirect('seller_dashboard')
    else:
        return redirect('login')

@login_required
def buyer_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    wallets = Wallet.objects.filter(user_profile=profile)
    selected_wallet = request.session.get('selected_wallet')
    # Handle wallet selection
    if request.method == 'POST':
        if 'add_wallet' in request.POST:
            wallet_address = request.POST.get('wallet_address')
            if wallet_address:
                if not Wallet.objects.filter(wallet_address=wallet_address).exists():
                    Wallet.objects.create(user_profile=profile, wallet_address=wallet_address)
                    wallets = Wallet.objects.filter(user_profile=profile)
                    messages.success(request, f"Wallet {wallet_address} added to your dashboard.")
                else:
                    messages.error(request, f"Wallet {wallet_address} already exists in the system.")
        elif 'select_wallet' in request.POST:
            selected_wallet = request.POST.get('select_wallet')
            request.session['selected_wallet'] = selected_wallet
        elif 'disconnect_wallet' in request.POST:
            request.session['selected_wallet'] = None
            selected_wallet = None
        elif 'delete_wallet' in request.POST:
            wallet_address = request.POST.get('delete_wallet')
            wallet = wallets.filter(wallet_address=wallet_address).first()
            if wallet:
                wallet.delete()
                wallets = Wallet.objects.filter(user_profile=profile)
                messages.success(request, f"Wallet {wallet_address} deleted from your dashboard.")
                if selected_wallet == wallet_address:
                    request.session['selected_wallet'] = None
                    selected_wallet = None
    return render(request, 'dashboard/buyer_dashboard.html', {
        'profile': profile,
        'wallets': wallets,
        'selected_wallet': selected_wallet,
    })

@login_required
def seller_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    wallets = Wallet.objects.filter(user_profile=profile)
    selected_wallet = request.session.get('selected_wallet')
    # Handle wallet selection
    if request.method == 'POST':
        if 'add_wallet' in request.POST:
            wallet_address = request.POST.get('wallet_address')
            # if wallet_address and not wallets.filter(wallet_address=wallet_address).exists():
            #     Wallet.objects.create(user_profile=profile, wallet_address=wallet_address)
            #     wallets = Wallet.objects.filter(user_profile=profile)

            if wallet_address:
                if not Wallet.objects.filter(wallet_address=wallet_address).exists():
                    Wallet.objects.create(user_profile=profile, wallet_address=wallet_address)
                    wallets = Wallet.objects.filter(user_profile=profile)
                    messages.success(request, f"Wallet {wallet_address} added to your dashboard.")
                else:
                    messages.error(request, f"Wallet {wallet_address} is already linked to another user.")

        elif 'select_wallet' in request.POST:
            selected_wallet = request.POST.get('select_wallet')
            request.session['selected_wallet'] = selected_wallet
        elif 'disconnect_wallet' in request.POST:
            request.session['selected_wallet'] = None
            selected_wallet = None
    return render(request, 'dashboard/seller_dashboard.html', {
        'profile': profile,
        'wallets': wallets,
        'selected_wallet': selected_wallet,
        'contract_address': '0x5F40bEeb31D78474a33775Abe9Bd85574C76dafB',
        'contract_abi': json.dumps(json.loads(config('CONTRACT_ABI'))),
    })

@login_required
def producer_profile(request, address):
    from accounts.models import Wallet

    try:
        wallet = Wallet.objects.get(wallet_address=address)
        profile = wallet.user_profile
    except Wallet.DoesNotExist:
        wallet = None
        profile = None
    user_profile = UserProfile.objects.get(user=request.user)
    # Chat
    if request.method == 'POST' and 'send_message' in request.POST:
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            Message.objects.create(
                sender=user_profile,
                receiver=profile,
                text=message_form.cleaned_data['text']
            )
            return redirect('producer_profile', address=address)
    else:
        message_form = MessageForm()
    # Rating
    if request.method == 'POST' and 'submit_rating' in request.POST:
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            Rating.objects.create(
                rater=user_profile,
                ratee=profile,
                score=rating_form.cleaned_data['score'],
                comment=rating_form.cleaned_data['comment']
            )
            return redirect('producer_profile', wallet_address= address)
    else:
        rating_form = RatingForm()
    # Message history
    messages = Message.objects.filter(sender=user_profile, receiver=profile) | Message.objects.filter(sender=profile, receiver=user_profile)
    messages = messages.order_by('timestamp')
    # Average rating
    avg_rating = Rating.objects.filter(ratee=profile).aggregate(Avg('score'))['score__avg']
    ratings = Rating.objects.filter(ratee=profile).order_by('-timestamp')
    return render(request, 'dashboard/producer_profile.html', {
        'profile': profile,
        'message_form': message_form,
        'messages': messages,
        'rating_form': rating_form,
        'avg_rating': avg_rating,
        'ratings': ratings,
        'contract_address': '0x5F40bEeb31D78474a33775Abe9Bd85574C76dafB',
        'contract_abi': json.dumps(json.loads(config('CONTRACT_ABI'))),
        'wallet': wallet,
        'profile_address': address,
    })

@login_required
def consumer_profile(request, wallet_address):
    try:
        profile = UserProfile.objects.get(wallet_address=wallet_address, role='buyer')
    except UserProfile.DoesNotExist:
        profile = None
    user_profile = UserProfile.objects.get(user=request.user)
    # Chat
    if request.method == 'POST' and 'send_message' in request.POST:
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            Message.objects.create(
                sender=user_profile,
                receiver=profile,
                text=message_form.cleaned_data['text']
            )
            return redirect('consumer_profile', wallet_address=wallet_address)
    else:
        message_form = MessageForm()
    # Rating
    if request.method == 'POST' and 'submit_rating' in request.POST:
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            Rating.objects.create(
                rater=user_profile,
                ratee=profile,
                score=rating_form.cleaned_data['score'],
                comment=rating_form.cleaned_data['comment']
            )
            return redirect('consumer_profile', wallet_address=wallet_address)
    else:
        rating_form = RatingForm()
    # Message history
    messages = Message.objects.filter(sender=user_profile, receiver=profile) | Message.objects.filter(sender=profile, receiver=user_profile)
    messages = messages.order_by('timestamp')
    # Average rating
    avg_rating = Rating.objects.filter(ratee=profile).aggregate(Avg('score'))['score__avg']
    ratings = Rating.objects.filter(ratee=profile).order_by('-timestamp')
    return render(request, 'dashboard/consumer_profile.html', {
        'profile': profile,
        'message_form': message_form,
        'messages': messages,
        'rating_form': rating_form,
        'avg_rating': avg_rating,
        'ratings': ratings,
    })
