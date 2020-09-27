"""dbhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from apps.schema.views import ColumnListView, TableAutocomplete

admin.site.site_header = 'DBHub'

urlpatterns = [
    url(r"^$", ColumnListView.as_view(), name="index"),
    url(r'^autocomplete/$', TableAutocomplete.as_view(), name='table-autocomplete'),
]

if settings.ENABLE_OAUTH:
    old_admin_login = admin.site.login
    admin.site.login = login_required(admin.site.login)
    urlpatterns += [
        url(r'^admin-login/', old_admin_login),
        url(r'^oauth/', include('oauthadmin.urls')),
    ]
    settings.LOGIN_URL = '/oauth/login/'
    settings.LOGOUT_REDIRECT_URL = '/oauth/logout_redirect/'

urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
]
