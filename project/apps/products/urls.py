from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"), 
    path("productos/", views.ProductListView.as_view(), name="products"),
    path("productos/lista/", views.LoadProductListView.as_view(), name="product_list"),
    path('productos/<slug:slug>/', views.ProductListByCategoryView.as_view(), name='products_by_category'),
    path("productos/lista/<slug:slug>/", views.LoadProductListByCategoryView.as_view(), name="product_list_by_category"),
    path("productos/crear/", views.ProductCreateView.as_view(), name="product_create"),
    path("productos/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("productos/actualizar/<slug:slug>/", views.ProductUpdateView.as_view(), name="product_update"),
    path("productos/confirmar/eliminar/<slug:slug>/", views.ProductConfirmActionView.as_view(), name="product_confirm_delete"),
    path("productos/eliminar/<slug:slug>/", views.ProductDeleteView.as_view(), name="product_delete"),
]