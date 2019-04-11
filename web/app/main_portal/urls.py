from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('garage/', include('garage.urls')),
    path('', include('garage.urls')),
]
