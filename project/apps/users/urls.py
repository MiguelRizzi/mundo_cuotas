from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

urlpatterns = [
    path("iniciar-sesion/", views.CustomLoginView.as_view(), name="login"),
    path("cerrar-sesion/", views.CustomLogoutView.as_view(), name="logout"),
    path('cambiar-contraseña/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path("avatar/<int:pk>/", views.AvatarDetailView.as_view(), name="avatar_detail"),
    path("avatar/crear/", views.AvatarCreateView.as_view(), name="avatar_create"),
    path("avatar/actualizar/<int:pk>/", views.AvatarUpdateView.as_view(), name="avatar_update"),
    path("avatar/confirmar/eliminar/<int:pk>/", views.AvatarConfirmActionView.as_view(), name="avatar_confirm_delete"),
    path("avatar/eliminar/<int:pk>/", views.AvatarDeleteView.as_view(), name="avatar_delete"),
    path("navbar/", TemplateView.as_view(template_name="components/navbar.html"), name="load_navbar"),
        #Message
    path('mensajes/', views.MessageListView.as_view(), name='message_list'),
    path('mensajes/listar/', views.LoadMessageListView.as_view(), name='load_message_list'),
    path('mensajes/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('mensajes/crear/', views.MessageCreateView.as_view(), name='message_create'),
    path('mensajes/confirmar/actualizar/<int:pk>/', views.MessageConfirmActionView.as_view(), name='message_confirm_update'),
    path('mensajes/actualizar/<int:pk>/', views.MessageUpdateView.as_view(), name='message_update'),
    path('mensajes/confirmar/eliminar/<int:pk>/', views.MessageConfirmActionView.as_view(), name='message_confirm_delete'),
    path('mensajes/eliminar/<int:pk>/', views.MessageDeleteView.as_view(), name='message_delete'),
]