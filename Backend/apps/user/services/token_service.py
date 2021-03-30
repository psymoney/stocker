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
    def create(self, email):
        payload = {"email": email}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ENCRYPTION_ALGORITHM)
        return token

    def validate(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ENCRYPTION_ALGORITHM)
            email = payload["email"]
        except jwt.exceptions.InvalidSignatureError:
            return InvalidSignatureError
        except jwt.exceptions.DecodeError:
            return DecodeError
        except jwt.exceptions.InvalidTokenError:
            return InvalidTokenError

        return None

    def parse_token(self, token):
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
        except jwt.exceptions.InvalidTokenError:
            return None
        return payload
