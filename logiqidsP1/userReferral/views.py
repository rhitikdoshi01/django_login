from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from logiqidsP1.models import User, UserReferralCode
from ..RequestValidator.validators import validate_request

@csrf_exempt
def get_referees(request):
    if request.method == "POST":
        required_fields = {
            "referral_code": str
        }
        data, error = validate_request(request, required_fields)
        if error:
            return error
        try:
            data = json.loads(request.body)
            referral_code = data.get("referral_code")

            if not referral_code:
                return JsonResponse({"error": "referral_code is required"}, status=400)
            referee_user = UserReferralCode.objects.filter(referral_code=referral_code).first()
            if referee_user:
                referee_id = referee_user.user_id
                referees = User.objects.filter(referred_by=referee_id)

                if referees.exists():
                    user_data = [
                        {
                            "username": user.username,
                            "emailID": user.email,
                            "registrationTimestamp": user.created_at,
                        }
                        for user in referees
                    ]
                    return JsonResponse({"referees": user_data}, status=200)
                else:
                    return JsonResponse({"referees":"No Referees Present for provided Referral Code"}, status=200)
            else:
                return JsonResponse({"Error":"No User Exists with provided Referral code"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        return JsonResponse({"error": "Only POST method allowed"}, status=405)