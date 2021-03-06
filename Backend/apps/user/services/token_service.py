import jwt
from ..models import User
SECRET_KEY = '1q2w3e4r!@#$'
ENCRYPTION_ALGORITHM = 'HS256'

AuthorizationDeniedError = 'authorization denied'


class TokenService:
    def create_token(self, email):
        token = jwt.encode({"email": email}, SECRET_KEY, algorithm=ENCRYPTION_ALGORITHM).decode('utf-8')
        return token

    def verify_token(self, token):
        try:
            email = jwt.decode(token, SECRET_KEY, algorithms=ENCRYPTION_ALGORITHM)["email"]
        except jwt.exceptions.DecodeError as err:
            return err
        except jwt.exceptions.InvalidTokenError as err:
            return err
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return AuthorizationDeniedError
        except Exception as err:
            return f"{err} error while verifying token"
        return None
