# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class SistemaempleoActividadeconomica(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.CharField(unique=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    esta_activa = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'SistemaEmpleo_actividadeconomica'


class SistemaempleoBuscador(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    cedula = models.CharField(max_length=15)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10)
    correo = models.CharField(max_length=254)
    usuario = models.OneToOneField('SistemaempleoUsuario', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'SistemaEmpleo_buscador'


class SistemaempleoEmpresa(models.Model):
    id = models.BigAutoField(primary_key=True)
    cedula = models.CharField(max_length=15)
    nombre_comercial = models.CharField(max_length=100)
    actividad_economica = models.ForeignKey(SistemaempleoActividadeconomica, models.DO_NOTHING)
    tipo_persona = models.CharField(max_length=20)
    razon_social = models.CharField(max_length=100)
    correo = models.CharField(max_length=254)
    provincia = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    calle = models.CharField(max_length=50)
    celular = models.CharField(max_length=15)
    usuario = models.OneToOneField('SistemaempleoUsuario', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'SistemaEmpleo_empresa'


class SistemaempleoUsuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    usuario = models.CharField(unique=True, max_length=50)
    clave = models.CharField(max_length=50)
    tipo_usuario = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'SistemaEmpleo_usuario'


class Solicitarempleo(models.Model):
    buscador = models.ForeignKey('Buscador', models.DO_NOTHING)
    cargo_deseado = models.CharField(max_length=100)
    nivel_estudios = models.CharField(max_length=100)
    experiencia_anios = models.IntegerField()
    habilidades = models.TextField(blank=True, null=True)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True) 
    disponibilidad = models.CharField(max_length=50, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    fecha_publicacion = models.DateField(blank=True, null=True)
    esta_activa = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SolicitarEmpleo'


class ActividadEconomica(models.Model):
    codigo = models.CharField(unique=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    esta_activa = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actividadeconomica'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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


class Notificacion(models.Model):
    buscador = models.ForeignKey(Buscador, models.DO_NOTHING)
    empleo = models.ForeignKey('Publicarempleo', models.DO_NOTHING)
    solicitud = models.ForeignKey('Solicitarempleo', models.DO_NOTHING, null=True, blank=True)
    fecha_aplicacion = models.DateTimeField(blank=True, null=True)
    leido = models.BooleanField(blank=True, null=True)
    mensaje = models.TextField(blank=True, null=True)
    respuesta = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'notificacion'


class Publicarempleo(models.Model):
    empresa = models.ForeignKey(Empresa, models.DO_NOTHING)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    requisitos = models.TextField(blank=True, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo_contrato = models.CharField(max_length=50, blank=True, null=True)
    modalidad = models.CharField(max_length=20, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    fecha_publicacion = models.DateField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    esta_activa = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'publicarempleo'


class Usuario(models.Model):
    usuario = models.CharField(unique=True, max_length=50)
    clave = models.CharField(max_length=50)
    tipo_usuario = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'usuario'
