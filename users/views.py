import json
import bcrypt, jwt

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError
from datetime               import datetime, timedelta

from users.models       import User
from users.validation   import validate_email, validate_password
from my_settings        import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)

            email         = data['email']
            password      = data['password']
            name          = data['name']
            address       = data.get('address', None)
            phone_number  = data.get('phone_number', None)
            gender        = data.get('gender', None)
            age           = data.get('age', None)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message" : "EMAIL_ALREADY_EXISTS"}, status=409)

            validate_email(email)
            validate_password(password)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email         = email,
                password      = hashed_password,
                name          = name,
                address       = address,
                phone_number  = phone_number,
                gender        = gender,
                age           = age
            )

            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"message": "DECODE_ERROR"}, status=400)

        except ValidationError as error:
            return JsonResponse({"message": error.message}, status=error.code)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email     = data['email']
            password  = data['password']
            user      = User.objects.get(email = email)

            payload = {
                'id' : user.id,
                'exp': datetime.utcnow()+timedelta(days=1)
            }
            access_token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

            if bcrypt.checkpw(password.encode('utf-8'),user.password.encode('utf-8')):
                return JsonResponse({'MESSAGE':'SUCCESS', 'ACCESS_TOKEN':access_token, 'NAME':user.name}, status=200)
            return JsonResponse({"MESSAGE":"INVALID_USER"},status=401)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"},status=400)
            
        except User.DoesNotExist:
            return JsonResponse({"MESSAGE":"INVALID_USER"},status=401)