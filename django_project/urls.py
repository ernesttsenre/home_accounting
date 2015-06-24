"""py URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers
from money.views import *

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'groups', GroupViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'goals', GoalViewSet)
# router.register(r'categories', CategoryViewSet)
# router.register(r'operations', OperationViewSet)
# router.register(r'transfers', TransferViewSet)

urlpatterns = [
    url(r'^', include('money.urls', namespace='money')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^admin/', include(admin.site.urls)),

    # AngularJS
    url(r'^angular/', include('angular.urls', namespace='angular')),

    # Django REST
    url(r'^api/', include(router.urls)),
]
