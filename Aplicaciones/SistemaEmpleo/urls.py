from django.urls import path
from Aplicaciones.SistemaEmpleo import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login-buscador/', views.login_buscador, name='login_buscador'),
    path('login-empresa/', views.login_empresa, name='login_empresa'),

    path('registro-buscador/', views.registro_buscador, name='registro_buscador'),
    path('registro-empresa/', views.registro_empresa, name='registro_empresa'),

    path('inicio-buscador/', views.inicio_buscador, name='inicio_buscador'),
    path('inicio-empresa/', views.inicio_empresa, name='inicio_empresa'),

    path('logout/', views.logout_usuario, name='logout'),

    # URL EMPRESA
    path('registrar-empleo/', views.registrar_empleo, name='registrar_empleo'),
    path('empleo/editar/<int:id>/', views.editar_empleo, name='editar_empleo'),
    path('empleo/eliminar/<int:id>/', views.eliminar_empleo, name='eliminar_empleo'),
    path('empleo/toggle-estado/<int:id>/', views.toggle_estado_empleo, name='toggle_estado_empleo'),

    # URL BUSCADOR
    path('registrar-solicitud/', views.registro_solicitud_empleo, name='registrar_solicitud'),
    path('solicitudes/editar/<int:id>/', views.editar_solicitud, name='editar_solicitud'),
    path('solicitudes/eliminar/<int:id>/', views.eliminar_solicitud, name='eliminar_solicitud'),

]
