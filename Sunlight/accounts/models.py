from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255, blank=True)
    district_state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=20, blank=True)
    # ... other existing fields ...
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    aadhar = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    country_code = models.CharField(max_length=5)
    mobile = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=255)
    pincode = models.CharField(max_length=6)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

class Rating(models.Model):
    rater = models.ForeignKey(UserProfile, related_name='given_ratings', on_delete=models.CASCADE)
    ratee = models.ForeignKey(UserProfile, related_name='received_ratings', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.score} stars from {self.rater} to {self.ratee}"

class Wallet(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='wallets', on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=42, unique=True)

    def __str__(self):
        return f"{self.wallet_address} (User: {self.user_profile.first_name} {self.user_profile.last_name})"
