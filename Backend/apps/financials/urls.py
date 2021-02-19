from django.urls import path, include
from . import views
from .views import *
from rest_framework.request import Request

urlpatterns = [
    path('', views.CompView.as_view()),
    #    path('financials/', views.ExternalAPIRequestView.as_view()),
]
