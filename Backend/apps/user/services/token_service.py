import jwt
from ..models import User
from . import sign_in_service
SECRET_KEY = '1q2w3e4r!@#$'
ENCRYPTION_ALGORITHM = 'HS256'

AuthorizationDeniedError = 'authorization denied'
InvalidTokenError = 'invalid token'
DecodeError = 'error while decoding token'
InvalidSignatureError = 'invalid signature'
ExpiredSignatureError = 'signature expired'


class TokenService:
    def create_token(self, email):
        payload = {"email": email}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ENCRYPTION_ALGORITHM)
        return token

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ENCRYPTION_ALGORITHM)
            email = payload["email"]
        except jwt.exceptions.InvalidSignatureError:
            return InvalidSignatureError
        except jwt.exceptions.DecodeError:
            return DecodeError
        except jwt.exceptions.InvalidTokenError:
            return InvalidTokenError
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return sign_in_service.UserNotFoundError
        except Exception as err:
            return f"{err} error while verifying token"
        return None

    def return_email(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ENCRYPTION_ALGORITHM)
            email = payload['email']
        except jwt.exceptions.InvalidSignatureError:
            return None
        except jwt.exceptions.DecodeError:
            return None
        except jwt.exceptions.InvalidTokenError:
            return None
        return email
