from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CompView.as_view()),
    #    path('financials/', views.ExternalAPIRequestView.as_view()),
]
