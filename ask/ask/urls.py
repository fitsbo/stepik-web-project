"""ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from qa import views

urlpatterns = [path('', views.home, name='home'),
               path('question/<int:pk>/', views.question, name='question'),
               path('ask/', views.ask, name='ask'),
               path('popular/', views.popular, name='popular'),
               path('signup/', views.signup, name='signup'),
               path('login/', views.login_view, name='login'),
               path('logout/', views.logout_view, name='logout'),
               path('new/', views.test, name='new'),
               ]
