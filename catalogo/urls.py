from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('publicar/', views.publicar_view, name='publicar'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('solicitar/<int:libro_id>/', views.solicitar_view, name='solicitar'),
    path('eliminar-libro/<int:libro_id>/', views.eliminar_libro_view, name='eliminar_libro'),
    # Materias
    path('materias/', views.materias_lista, name='materias_lista'),
    path('materias/<slug:slug>/', views.materias_libros, name='materias_libros'),
    # Mensajes
    path('mensajes/', views.mensajes_inbox, name='mensajes_inbox'),
    path('mensajes/enviados/', views.mensajes_enviados, name='mensajes_enviados'),
    path('mensajes/enviar/', views.mensajes_enviar, name='mensajes_enviar'),
    path('mensajes/enviar/<int:libro_id>/', views.mensajes_enviar, name='mensajes_enviar_libro'),
    path('mensajes/<int:mensaje_id>/', views.mensajes_hilo, name='mensajes_hilo'),
    # Ajustes
    path('ajustes/', views.ajustes_perfil, name='ajustes_perfil'),
    path('ajustes/password/', views.ajustes_password, name='ajustes_password'),
    # Páginas estáticas
    path('acerca/', views.pagina_acerca, name='pagina_acerca'),
    path('faq/', views.pagina_faq, name='pagina_faq'),
    path('terminos/', views.pagina_terminos, name='pagina_terminos'),
    path('contacto/', views.pagina_contacto, name='pagina_contacto'),
    # Favoritos
    path('favoritos/toggle/<int:libro_id>/', views.favoritos_toggle, name='favoritos_toggle'),

    path('libro/<int:pk>/mapa/', views.mapa_intercambio, name='mapa_intercambio'),

]
