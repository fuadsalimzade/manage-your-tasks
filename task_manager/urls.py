"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from task import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # auth
    path("signup/", views.signupuser, name="signupuser"),
    path("logout/", views.logoutuser, name="logoutuser"),
    path("login/", views.loginuser, name="loginuser"),
    # user
    path("current/", views.currenttasks, name="currenttasks"),
    path("current/<int:task_pk>", views.currenttask, name="currenttask"),
    path("current/<int:task_pk>/complete>", views.completecurrenttask, name="completecurrenttask"),
    path("current/<int:task_pk>/delete>", views.deletecurrenttask, name="deletecurrenttask"),
    path("createtask/", views.createtask, name="createtask"),
    path("completedtasks/", views.completedtasks, name="completedtasks"),
    path("completed/<int:task_pk>", views.completedtask, name="completedtask"),
    path("", views.home, name="home"),
]
