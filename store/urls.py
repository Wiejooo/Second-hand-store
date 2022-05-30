from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from cloth_app.views import MainView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("shop/", include("cloth_app.urls")),
    path("", MainView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
