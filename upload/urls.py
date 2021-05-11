from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import image_upload_view

urlpatterns = [

    path('upload/', image_upload_view, name='upload'),] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)