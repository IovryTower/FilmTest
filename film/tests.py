
# Create your tests here.
from django.urls import path

from . import views

urlpatterns = [
    path('film/', views.hell),
]