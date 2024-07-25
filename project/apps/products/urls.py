from django.urls import path
from . import views

urlpatterns = [
    path("productos/crear/", views.ProductCreateView.as_view(), name="product_create"),
    path("", views.ProductListView.as_view(), name="index"),
    path("productos/", views.ProductListView.as_view(template_name="products/product_list.html"), name="product_list"),
    path("cargar/productos/", views.LoadProductListView.as_view(), name="load_product_list"),
    path("sobre-nosotros/", views.AboutView.as_view(), name="about"),

    path("contacto/", views.ContactView.as_view(), name="contact"),
    path("productos/<slug:slug>/", views.ProductDetailView.as_view(template_name="products/product_detail.html"), name="product_detail"),


    path("subcategorias/cargar/", views.LoadSubcategoriesView.as_view(), name="load_subcategories"),
    path("administracion/productos/", views.ProductListAdminView.as_view(), name='product_list_admin'),
    path("administracion/cargar/productos/", views.LoadProductListAdminView.as_view(), name='load_product_list_admin'),
    
    path("administracion/productos/<slug:slug>/", views.ProductDetailAdminView.as_view(), name="product_detail_admin"),

    path("productos/actualizar/<slug:slug>/", views.ProductUpdateView.as_view(), name="product_update"),
    path("productos/confirmar/eliminar/<slug:slug>/", views.ProductConfirmActionView.as_view(), name="product_confirm_delete"),
    path("productos/eliminar/<slug:slug>/", views.ProductDeleteView.as_view(), name="product_delete"),

    path("subcategorias/cargar/<slug:slug>/", views.LoadProductSubcategoriesView.as_view(), name="load_product_subcategories"),
]