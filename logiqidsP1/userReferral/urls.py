from django.urls import path
from .views import get_referees

urlpatterns = [
    path("getReferees/", get_referees, name="get_referees"),
]
