from django.urls import path

from . import views

urlpatterns = [
    path('reports/', views.CompanyLookupView.as_view()),
]
