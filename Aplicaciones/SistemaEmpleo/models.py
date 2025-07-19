# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ActividadEconomica(models.Model):
    codigo = models.CharField(unique=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    esta_activa = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actividadeconomica'


class Buscador(models.Model):
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)
    nombre = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10)
    correo = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'buscador'


class Empresa(models.Model):
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)
    cedula = models.CharField(max_length=15)
    nombre_comercial = models.CharField(max_length=100)
    actividad_economica = models.ForeignKey(ActividadEconomica, models.DO_NOTHING, blank=True, null=True)
    tipo_persona = models.CharField(max_length=20)
    razon_social = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    provincia = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    calle = models.CharField(max_length=50)
    celular = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'empresa'


class Usuario(models.Model):
    usuario = models.CharField(unique=True, max_length=50)
    clave = models.CharField(max_length=50)
    tipo_usuario = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'usuario'
