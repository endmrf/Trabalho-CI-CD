from django.contrib import admin
from django.urls import path
from example.views import example

urlpatterns = [
    path('admin/', admin.site.urls),
    path('example/', example),
]
