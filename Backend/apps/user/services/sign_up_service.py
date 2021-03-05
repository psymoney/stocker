from ..models import User
from django.core import validators as valid

DuplicateEmailExistError = 'duplicate email exists'
InvalidEmailError = 'invalid email format'
InvalidUserNameError = 'invalid name format'
InvalidPasswordError = 'invalid password format'


class SignUpService:
    def create_user_account(self, email, user_name, password):
        def check_duplicate(email):
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                return None
            except Exception as err:
                return f"{err} error while creating user for user email = {email}"
            return DuplicateEmailExistError

        def validate_email(email):
            if len(email) > 50:
                return InvalidEmailError
            try:
                valid.validate_email(email)
            except valid.ValidationError:
                return InvalidEmailError
            return None

        def validate_user_name(user_name):
            if len(user_name) < 1:
                return InvalidUserNameError
            return None

        def validate_password(password):
            if len(password) < 8:
                return InvalidPasswordError
            return None

        duplication = check_duplicate(email)
        if duplication:
            return duplication
        if validate_email(email):
            return InvalidEmailError
        if validate_user_name(user_name):
            return InvalidUserNameError
        if validate_password(password):
            return InvalidPasswordError
        try:
            User.objects.create(email=email, user_name=user_name, password=password)
        except Exception as err:
            return f"{err} error while creating user account"
        return None

