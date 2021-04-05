from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('financial/', include("apps.financials.urls")),
    path('user/', include("apps.user.urls")),
    path('favorites/', include("apps.favorite.urls")),
]
