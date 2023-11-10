from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("accounts/", include("modules.accounts.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]


admin.site.site_header = "Dj Starter Admin"
admin.site.site_title = "Dj Starter Admin Portal"
admin.site.index_title = "Welcome to Dj Starter Portal"
