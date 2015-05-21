from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from money.views import OperationDetail, OperationCreate, AccountList, AccountDetail, TransferCreate

urlpatterns = [
    url(r'^$', login_required(AccountList.as_view()), name='index'),
    url(r'^account/(?P<pk>[0-9]+)$', login_required(AccountDetail.as_view()), name='account'),
    url(r'^operation/(?P<pk>[0-9]+)$', login_required(OperationDetail.as_view()), name='operation'),
    url(r'^operation/create/(?P<account_id>[0-9]+)$', login_required(OperationCreate.as_view()), name='create_operation'),
    url(r'^transfer/create/$', login_required(TransferCreate.as_view()), name='create_transfer'),
]