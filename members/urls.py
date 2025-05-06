from django.urls import path
from .views import sign_up, log_in, sign_page, log_page, logout_user

urlpatterns = [
    path('sign-up/', sign_up, name='sign_up'),
    path('log-in/', log_in, name='log_in'),
    path('log-out', logout_user, name='logout'),
    path('sign/', sign_page, name='sign'),
    path('log/', log_page, name='log')
]
