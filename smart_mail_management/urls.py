"""
URL configuration for smart_mail_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from mail_manager_backend.views import get_tasks, hello

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        view=hello,
    ),
    path(
        "task",
        view=get_tasks,
    ),
    path(
        "gmail/",
        include("mail_manager_backend.routes.api_endpoints", namespace="gmail"),
    ),
]
