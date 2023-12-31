from django.urls import path
from . import views

urlpatterns = [
    path('heart', views.heart, name="heart"),
    path('diabetes', views.diabetes, name="diabetes"),
    path('breast', views.breast, name="breast"),
    path('calories', views.calories, name="calories"),
    path('', views.home, name="home"),
]