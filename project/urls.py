from django.conf.urls import include, url
from app.views import NotFoundView

handler404 = NotFoundView.as_view()

urlpatterns = [
    url(r'', include('app.urls'))
]
