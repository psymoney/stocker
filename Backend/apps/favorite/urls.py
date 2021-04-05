from django.urls import path
from . import views

urlpatterns = [
    path('', views.FavoriteView.as_view()),
    path('report/', views.FavoriteReportView.as_view()),
]