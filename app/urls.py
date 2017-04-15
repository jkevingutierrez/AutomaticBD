from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from app.views import IndexView, ServiceView, FileView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'api', csrf_exempt(ServiceView.as_view()), name='service'),
    url(r'file', csrf_exempt(FileView.as_view()), name='file')
]
