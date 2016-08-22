from django.conf.urls import url
from api.views import common

urlpatterns = [
    url(r'^login/$', common.Login.as_view(), name='home')
]
