from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Product
    
class ProductSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.2
    def items(self):
        return ['products:contact']
    def location(self, item):
        return reverse(item)
    
class ContactSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1
    def items(self):
        return ['products:product_list']
    def location(self, item):
        return reverse(item)

    
class ProductDetailSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
    