from django.db import models


class Usuario(models.Model):
    TIPO_USUARIO = [
        ('buscador', 'Buscador de Empleo'),
        ('empresa', 'Empresa'),
    ]
    usuario = models.CharField(max_length=50, unique=True)
    clave = models.CharField(max_length=50)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO)

    def __str__(self):
        return f'{self.usuario} - {self.get_tipo_usuario_display()}'
