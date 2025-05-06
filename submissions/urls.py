from django.urls import path
from .views import run_diagnosis

urlpatterns = [
    path('run-diagnosis', run_diagnosis, name='run_diagnosis'),
]