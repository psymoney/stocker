from ..models import User

UserNotFoundError = 'user not found'
WrongPasswordError = 'wrong password'


class SignInService:
    def sign_in(self, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return UserNotFoundError
        if user.password != password:
            return WrongPasswordError
        return None
