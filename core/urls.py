"""
URL configuration for core project.

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

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

from applications.accounts.views import UserLoginView, UserLogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("applications.api_overview.urls")),
    path("api/users/", include("applications.accounts.urls")),
    path("api/auth/login/", UserLoginView.as_view(), name="obtain_auth_token"),
    path("api/auth/logout/", UserLogoutView.as_view(), name="logout_view"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/projects/", include("applications.projects.urls")),
    path("api/tasks/", include("applications.tasks.urls")),
] + debug_toolbar_urls()
