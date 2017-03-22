from django.conf.urls import url
from app.views import IndexView, ServiceView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'api', csrf_exempt(ServiceView.as_view()), name='service')
]