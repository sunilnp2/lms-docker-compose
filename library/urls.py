from django.urls import path, include
app_name = 'library'

urlpatterns = [

# Adding url for Custom Library API directory url on Django app
    path('api/', include('library.api.urls')),

]
