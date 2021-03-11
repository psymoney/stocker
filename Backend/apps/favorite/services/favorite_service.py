from ..models import Favorite as FavoriteModel
from apps.user.models import User

FavoriteAlreadyExistError = 'favorite already exists'
UserNotFound = 'user not found'


class Favorite:
    def __init__(self, id, corporate_name, corporate_code, consolidation):
        self.id = id
        self.corporate_name = corporate_name
        self.corporate_code = corporate_code
        self.consolidation = consolidation

    def to_JSON_response(self):
        return {
            "id": self.id,
            "corporateName": self.corporate_name,
            "corporateCode": self.corporate_code,
            "consolidation": self.consolidation
        }

class FavoriteService:

    def check_duplicate(self, email, corporate_name, corporate_code, consolidation):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return UserNotFound
        try:
            FavoriteModel.objects.get(user_email=user,
                                      corporate_name=corporate_name,
                                      corporate_code=corporate_code,
                                      consolidation=consolidation)
        except FavoriteModel.DoesNotExist:
            return None
        return FavoriteAlreadyExistError

    def create_favorite(self, email, corporate_name, corporate_code, consolidation):
        user = User.objects.get(email=email)
        try:
            FavoriteModel.objects.create(user_email=user,
                                         corporate_name=corporate_name,
                                         corporate_code=corporate_code,
                                         consolidation=consolidation)
        # TODO(SY): add predictable exceptions
        except Exception as err:
            return f"{err} error while creating favorite"
        return None

    def delete_favorite(self, email, corporate_name, corporate_code, consolidation):
        user = User.objects.get(email=email)
        try:
            favorite = FavoriteModel.objects.get(user_email=user,
                                                 corporate_name=corporate_name,
                                                 corporate_code=corporate_code,
                                                 consolidation=consolidation)
            favorite.delete()
        # TODO(SY): add predictable exceptions
        except Exception as err:
            return f"{err} error while deleting favorite"
        return None

    def get_favorites(self, email):
        result = []
        user = User.objects.get(email=email)
        try:
            favorites = FavoriteModel.objects.filter(user_email=user)
        # TODO(SY): add predictable exceptions
        except Exception as err:
            return f"{err} error while getting favorites"

        for favorite in favorites:
            favorite = Favorite(favorite.id, favorite.corporate_name, favorite.corporate_code, favorite.consolidation)
            result.append(favorite.to_JSON_response())

        return result
