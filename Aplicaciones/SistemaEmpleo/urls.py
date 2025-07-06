from django.contrib import admin
from django.urls import path
from Aplicaciones.SistemaEmpleo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('login-buscador/', views.login_buscador, name='login_buscador'),
    path('login-empresa/', views.login_empresa, name='login_empresa'),

    path('registro-buscador/', views.registro_buscador, name='registro_buscador'),
    path('registro-empresa/', views.registro_empresa, name='registro_empresa'),

    path('inicio-buscador/', views.inicio_buscador, name='inicio_buscador'),
    path('inicio-empresa/', views.inicio_empresa, name='inicio_empresa'),
]
