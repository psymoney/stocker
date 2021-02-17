from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('internal/', views.ErrorView.as_view()),
]
