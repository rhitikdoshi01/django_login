import random
import string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import json
from django.contrib.auth.hashers import make_password
from logiqidsP1.models import User, UserReferralCode
from ..RequestValidator.validators import validate_request


def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

@csrf_exempt
def register_user(request):
    if request.method == "OPTIONS":
        return JsonResponse({"message": "OK"}, status=200)
    elif request.method == "POST":
        required_fields = {
            "username": str,
            "email": str,
            "mobile_number": str,
            "city": str,
            "password": str,
            "referral_code": str
        }

        data, error = validate_request(request, required_fields)
        if error:
            return error
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            mobile_number = data.get("mobile_number")
            city = data.get("city")
            referral_code = data.get("referral_code")
            password = data.get("password")

            if not password:
                return JsonResponse({"error": "Password is required"}, status=400)
            check_user = User.objects.filter(email=email).first()
            if check_user:
                return JsonResponse({error:"Email Id already exists"}, status=400)

            hashed_password = make_password(password)

            referred_by = None
            if referral_code:
                try:
                    referred_user = UserReferralCode.objects.get(referral_code=referral_code).user_id
                    referred_by = referred_user
                except UserReferralCode.DoesNotExist:
                    return JsonResponse({"error": "Invalid referral code"}, status=400)

            user = User.objects.create(
                username=username,
                email=email,
                mobile_number=mobile_number,
                city=city,
                referred_by=referred_by,
                password=hashed_password
            )

            unique_referral_code = generate_referral_code()
            while UserReferralCode.objects.filter(referral_code=unique_referral_code).exists():
                unique_referral_code = generate_referral_code()

            UserReferralCode.objects.create(user_id=user.user_id, referral_code=unique_referral_code)

            return JsonResponse({"message": "User registered successfully", "user_id": user.user_id, "referral_code": unique_referral_code}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        required_fields = {
            "loginUsername": str,
            "password": str
        }
        data, error = validate_request(request, required_fields)
        if error:
            return error
        try:
            data = json.loads(request.body)
            username = data.get("loginUsername")
            password = data.get("password")
            if not password or not username:
                return JsonResponse({"error":"Password / Email cannot be empty"},status=400)
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return JsonResponse({"error": "Invalid email or password"}, status=400)

            if check_password(password, user.password):
                return JsonResponse({"message": "Login successful", "user_id": user.user_id}, status=200)
            else:
                return JsonResponse({"error": "Invalid email or password"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
