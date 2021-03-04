from ..models import User
from django.core import validators as valid

DuplicateEmailExistError = 'Duplicate email exists'
InvalidEmailError = 'Invalid email'
InvalidUserNameError = 'Invalid name'
InvalidPasswordError = 'Invalid password'


class SignUpService:
    def sign_up(self, email, user_name, password):
        def duplication_check(email):
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return True
            except User.MultipleObjectsReturned:
                return DuplicateEmailExistError
            return DuplicateEmailExistError

        def validity_check(email, user_name, password):
            def email_check(email):
                if len(email) > 50:
                    return InvalidEmailError
                try:
                    emailcheck = valid.validate_email(email)
                except valid.ValidationError:
                    return InvalidEmailError
                return True

            def user_name_check(user_name):
                if len(user_name) < 1 or len(user_name) > 20:
                    return InvalidUserNameError
                return True

            def password_check(password):
                if len(password) < 8 or len(password) > 16:
                    return InvalidPasswordError
                return True

            if email_check(email) != True:
                return InvalidEmailError
            if user_name_check(user_name) != True:
                return InvalidUserNameError
            if password_check(password) != True:
                return InvalidPasswordError
            return True

        validity = validity_check(email, user_name, password)
        if validity != True:
            return validity
        duplication = duplication_check(email)
        if duplication == True:
            User.objects.create(email=email, user_name=user_name, password=password)
            return True
        return duplication
