from django.urls import path
from . import views

urlpatterns = [
    # Página principal - Directorio
    path('', views.directorio_army, name='directorio_army'),
    
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Perfil
    path('perfil/<str:username>/', views.ver_perfil, name='ver_perfil'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    
    # Fotos
    path('subir-foto/', views.subir_foto, name='subir_foto'),
    path('eliminar-foto/<int:foto_id>/', views.eliminar_foto, name='eliminar_foto'),
    
    # Listas
    path('crear-lista/', views.crear_lista, name='crear_lista'),
    path('editar-lista/<int:lista_id>/', views.editar_lista, name='editar_lista'),
    path('eliminar-lista/<int:lista_id>/', views.eliminar_lista, name='eliminar_lista'),
]