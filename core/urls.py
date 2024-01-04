from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="index"),
    path(
        "find_your_perfect_glasses/",
        views.find_your_perfect_glasses,
        name="find_your_perfect_glasses",
    ),
    path("submit_image_url/", views.submit_image_url, name="submit_image_url"),
    path("result/", views.result, name="result"),
    path("result_upload/", views.result_upload, name="result_upload"),
    path("upload_image/", views.upload_image, name="upload_image"),
    path("captured_image/", views.captured_image, name="captured_image"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.RESULT_URL, document_root=settings.RESULT_ROOT)
