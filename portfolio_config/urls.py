from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize Django Admin Header
admin.site.site_header = "ISREL | Portfolio Administration"
admin.site.site_title = "ISREL Portfolio Admin"
admin.site.index_title = "Manage Portfolio Content, Skills & Inquiries"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
