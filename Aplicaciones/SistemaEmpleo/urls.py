from django.contrib import admin
from django.urls import path
from Aplicaciones.SistemaEmpleo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login y registro
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),

    # Pantallas de inicio
    path('inicio-buscador/', views.inicio_buscador, name='inicio_buscador'),
    path('inicio-empresa/', views.inicio_empresa, name='inicio_empresa'),
]
