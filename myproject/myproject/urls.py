from django.conf.urls import include, url

urlpatterns = [
    url(r'^myapp/', include('myapp.urls'))
]