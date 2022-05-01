import jwt

from users.models import User
from django.http  import JsonResponse
from django.conf  import settings

def login_decorator(func) :
    def wrapper(self, request, *args, **kwrags) :
        try:
            token = request.headers.get('Authorization', None)
            payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
            request.user = User.objects.get(id=payload['id'])

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=401)

        except jwt.exceptions.DecodeError :
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)
        
        except jwt.ExpiredSignatureError :
            return JsonResponse({'message':'EXPIRED_TOKEN'}, status=401)

        except jwt.InvalidSignatureError:
            return JsonResponse({'message' : 'invalid_signature'}, status=401)
        
        return func(self, request, *args, **kwrags)
    
    return wrapper