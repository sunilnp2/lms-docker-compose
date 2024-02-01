from django.urls import path, include
from authentication.api.views import SignUpSerializerView, GetUserView, LoginSerializerView

urlpatterns = [
    path('signup/', SignUpSerializerView.as_view(), name = "signup"),
    # for get user
    path('getalluser/',GetUserView.as_view(), name = "getalluser"),
    path('getuser/<pk>/',GetUserView.as_view(), name = "getuser"),

    path('login/',LoginSerializerView.as_view(), name='login'),
]
