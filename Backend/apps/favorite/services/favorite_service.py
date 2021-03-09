from ..models import Favorite
from apps.user.models import User

DuplicateExistError = 'duplicate favorite exist'
DoesNotExistError = 'list does not exist'


class FavoriteReport:
    def __init__(self, id, corporate_name, corporate_code, consolidation):
        self.id = id
        self.corporate_name = corporate_name
        self.corporate_code = corporate_code
        self.consolidation = consolidation

    def __str__(self):
        return 'email = {} corporate_name = {} corporate_code = {} consolidation = {}'.format(self.id, self.corporate_code, self.corporate_name, self.consolidation)

    def to_JSON_response(self):
        return {
            "id": self.id,
            "corporation_name": self.corporate_name,
            "corporation_code": self.corporate_code,
            "consolidation": self.consolidation
        }

class FavoriteService:

    def check_duplicate(self, email, corporate_name, corporate_code, consolidation):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return DoesNotExistError
        try:
            Favorite.objects.get(user_email=user,
                                 corporate_name=corporate_name,
                                 corporate_code=corporate_code,
                                 consolidation=consolidation)
        except Favorite.DoesNotExist:
            return None
        return DuplicateExistError

    def create_favorite(self, email, corporate_name, corporate_code, consolidation):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return DoesNotExistError
        try:
            Favorite.objects.create(user_email=user,
                                    corporate_name=corporate_name,
                                    corporate_code=corporate_code,
                                    consolidation=consolidation)
            print("creation success")
        # TODO(SY): add predictable exceptions
        except Exception as err:
            return f"{err} error while creating favorite"
        return None

    def delete_favorite(self, email, corporate_name, corporate_code, consolidation):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return DoesNotExistError
        try:
            favorite = Favorite.objects.get(user_email=user,
                                    corporate_name=corporate_name,
                                    corporate_code=corporate_code,
                                    consolidation=consolidation)
            favorite.delete()
            print("deletion success")
        # TODO(SY): add predictable exceptions
        except Exception as err:
            return f"{err} error while deleting favorite"
        return None

    def get_favorites(self, email):
        favorites = []
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return DoesNotExistError
        try:
            favorite_group = Favorite.objects.filter(user_email=user)
        # TODO(SY): add predictable exceptions
        except Exception as err:
            return f"{err} error while deleting favorite"

        for favorite in favorite_group:
            favorite_report = FavoriteReport(favorite.id, favorite.corporate_name, favorite.corporate_code, favorite.consolidation)
            favorites.append(favorite_report.to_JSON_response())

        return favorites
