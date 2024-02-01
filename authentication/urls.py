app_name = 'authentication'
from django.urls import path, include

urlpatterns = [

    # Adding url for Custom API directory url on Django app
    path('api/', include('authentication.api.urls')),
]
