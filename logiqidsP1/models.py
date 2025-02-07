from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=255)
    mobile_number = models.BigIntegerField(unique=True)
    city = models.CharField(max_length=150)
    referred_by = models.IntegerField(null=True, blank=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_details"


class UserReferralCode(models.Model):
    # user_id = models.OneToOneField(User,on_delete=models.CASCADE)
    referral_code = models.CharField(unique=True, max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        db_table = "user_referral_code"