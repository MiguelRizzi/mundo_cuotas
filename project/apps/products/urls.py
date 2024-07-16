from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"), 
    path("contacto/", views.ContactView.as_view(), name="contact"),

    path("productos/", views.ProductListView.as_view(), name="product_list"),
    path('productos/administracion/', views.ProductListAdminView.as_view(), name='product_list_admin'),
    path("productos/cargar/", views.LoadProductListAdminView.as_view(), name="load_product_list"),
    path('productos/categorias/<slug:slug>/', views.ProductListByCategoryView.as_view(), name='product_list_by_category'),
    path('productos/categorias/cargar/<slug:slug>/', views.LoadProductListByCategoryView.as_view(), name='load_product_list_by_category'),
    path("productos/crear/", views.ProductCreateView.as_view(), name="product_create"),
    path("productos/<slug:slug>/", views.ProductDetailView.as_view(template_name="products/product_detail.html"), name="product_detail"),
    path("productos/admin/<slug:slug>/", views.ProductDetailView.as_view(template_name="products/product_detail_admin.html"), name="product_detail_admin"),

    path("productos/actualizar/<slug:slug>/", views.ProductUpdateView.as_view(), name="product_update"),
    path("productos/confirmar/eliminar/<slug:slug>/", views.ProductConfirmActionView.as_view(), name="product_confirm_delete"),
    path("productos/eliminar/<slug:slug>/", views.ProductDeleteView.as_view(), name="product_delete"),
]