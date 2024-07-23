from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import sitemap

from .sitemaps import ProductSitemap, ContactSitemap, ProductDetailSitemap


sitemaps = {
    'products': ProductSitemap,
    'product_detail': ProductDetailSitemap,
    'contact': ContactSitemap,
}

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("", include(("users.urls", "users"))),
    path("", include(("products.urls", "products"))),

    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Valido en entorno de desarrollo: DEBUG= True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
