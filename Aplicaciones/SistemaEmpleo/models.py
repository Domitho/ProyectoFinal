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


class Buscador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=15)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10)
    correo = models.EmailField()

    def __str__(self):
        return self.usuario.usuario


class Empresa(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_comercial = models.CharField(max_length=100)
    actividad_economica = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=100)
    correo = models.EmailField()

    def __str__(self):
        return self.usuario.usuario
