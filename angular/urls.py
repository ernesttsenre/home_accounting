from django.conf.urls import url
from angular.views import MainPageView

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='index'),
]
