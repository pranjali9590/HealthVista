from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name = "index"),
    path('index1', views.index1, name = "index1"),
    path('ov', views.ov, name = "ov"),
    path('water', views.water, name = "water"),
    path('main', views.main, name = "main"),
    path('sp', views.sp, name = "sp"),
    path('rem', views.rem, name = "rem"),
    path('arti', views.arti, name = "arti"),
    path('trys', views.trys, name = "trys"),
    path('comm', views.comm, name = "comm"),
    path('try1', views.try1, name = "try1"),
    path('vegan', views.vegan, name = "vegan"),
    path('gluten', views.gluten, name = "gluten"),
    path('article', views.article, name = "article"),
    path('article_1', views.article_1, name = "article_1"),
    path('article_2', views.article_2, name = "article_2"),
    path('article_homepage', views.article_homepage, name = "article_homepage"),
    path('np1', views.np1, name = "np1"),
    path('bmi', views.bmi, name = "bmi"),
    path('mg', views.mg, name = "mg"),
    path('register', views.register, name = "register"),
    path('doctors', views.doctors, name = "doctors"),
    path('login', views.login, name = "login"),
    path('emergency', views.emergency, name = "emergency"),
    path('logout', views.logout, name = "logout"),
    path('contactus', views.contactus, name = "contactus"),
    path('onlineprescription', views.onlineprescription, name = "onlineprescription")
]