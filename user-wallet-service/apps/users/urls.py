from django.urls import path
from .views import register_view, LoginView, me_view

urlpatterns = [
    path('register', register_view, name='register'),
    path('login', LoginView.as_view(), name='token_obtain_pair'),
    path('me', me_view, name='me'),
]
