from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup),
    path('register', views.register),
    path('signin', views.signin),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
    path('account', views.account),
]