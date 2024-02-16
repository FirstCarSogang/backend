from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('firstCarSogang_home.urls'), name="home"),
    path('', include('firstCarSogang_signuplogin.urls')),
    path('tickets/', include('firstCarSogang_tickets.urls')),
]
