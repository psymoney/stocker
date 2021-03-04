from ..models import User

AuthenticationFailure = 'Failure'

class SignInService:
    def sign_in(self, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return AuthenticationFailure
        if user.password != password:
            return AuthenticationFailure
        return True
