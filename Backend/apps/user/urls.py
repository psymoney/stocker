from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SigninView.as_view()),
    path('signup/', view.SignupView.as_view())
]

