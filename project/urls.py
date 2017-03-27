from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from app.views import NotFoundView

handler404 = NotFoundView.as_view()

urlpatterns = [
    url(r'', include('app.urls'))
]

urlpatterns = [
    url(r'', include('app.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
