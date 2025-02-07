from rest_framework import serializers
from .models import User, UserReferralCode

class UserSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'mobile_number', 'city', 'referral_code']
