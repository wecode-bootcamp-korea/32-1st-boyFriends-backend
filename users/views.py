import json
import bcrypt

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from users.models       import User
from users.validation   import validate_email, validate_password

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)

            email         = data['email']
            password      = data['password']
            name          = data['name']
            address       = data['address']
            phone_number  = data['phone_number']
            gender        = data['gender']
            age           = data['age']

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

        except ValidationError as error:
            return JsonResponse({"message": error.message}, status=400)
