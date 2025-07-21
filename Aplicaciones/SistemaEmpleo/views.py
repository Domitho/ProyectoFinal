from ProyectoFinal import settings
from .models import Perfilbuscador, Perfilempresa, Usuario, Buscador, Empresa, ActividadEconomica, Publicarempleo, Solicitarempleo, Notificacion
from django.shortcuts import get_object_or_404, render, redirect
from decimal import Decimal, InvalidOperation
from django.core.mail import send_mail
from django.contrib import messages
from datetime import date
import datetime
from django.utils import timezone
import random
import string

# Funciones para generar credenciales automáticas
def generar_usuario(nombre, apellido):
    return f"{nombre[0].lower()}{apellido.lower()}{random.randint(1000, 9999)}"

def generar_contraseña():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Página de inicio
def home(request):
    return render(request, 'home.html')

# Login para buscadores
def login_buscador(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        clave = request.POST['clave']

        try:
            user = Usuario.objects.get(usuario=usuario, clave=clave, tipo_usuario='buscador')
            request.session['usuario_id'] = user.id  # Guardamos el usuario en sesión
            return redirect('inicio_buscador')
        except Usuario.DoesNotExist:
            return render(request, 'login_buscador.html', {'error': 'Usuario o clave incorrectos'})

    return render(request, 'buscador/login_buscador.html')


# Login para empresas
def login_empresa(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        clave = request.POST['clave']

        try:
            user = Usuario.objects.get(usuario=usuario, clave=clave, tipo_usuario='empresa')
            request.session['usuario_id'] = user.id  # Guardamos el usuario en sesión
            return redirect('inicio_empresa')
        except Usuario.DoesNotExist:
            return render(request, 'empresa/login_empresa.html', {'error': 'Usuario o clave incorrectos'})

    return render(request, 'empresa/login_empresa.html')

# Registro de buscador
def registro_buscador(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        cedula = request.POST['cedula']
        apellido = request.POST['apellido']
        fecha = request.POST['fecha']
        genero = request.POST['genero']
        correo = request.POST['correo']

        usuario_gen = generar_usuario(nombre, apellido)
        clave_gen = generar_contraseña()

        user = Usuario.objects.create(usuario=usuario_gen, clave=clave_gen, tipo_usuario='buscador')

        Buscador.objects.create(
            usuario=user,
            nombre=nombre,
            cedula=cedula,
            apellido=apellido,
            fecha_nacimiento=fecha,
            genero=genero,
            correo=correo
        )

        send_mail(
            'Registro exitoso - Sistema de Empleo',
            f'Bienvenido {nombre}, tus credenciales son:\nUsuario: {usuario_gen}\nContraseña: {clave_gen}',
            'tucorreo@gmail.com',
            [correo],
            fail_silently=False,
        )

        return redirect('login_buscador')

    return render(request, 'buscador/registro_buscador.html')

# Registro de empresa
def registro_empresa(request):
    actividades = ActividadEconomica.objects.filter(esta_activa=True)

    if request.method == 'POST':
        cedula = request.POST['cedula']
        nombre_comercial = request.POST['nombre']
        actividad_id = request.POST['actividad']
        tipo_persona = request.POST['persona']
        razon = request.POST['razon']
        correo = request.POST['correo']
        provincia = request.POST['provincia']
        ciudad = request.POST['ciudad']
        calle = request.POST['calle']
        celular = request.POST['celular']

        actividad_obj = ActividadEconomica.objects.get(id=actividad_id)

        usuario_gen = generar_usuario(nombre_comercial.split()[0], razon.split()[0])
        clave_gen = generar_contraseña()

        user = Usuario.objects.create(usuario=usuario_gen, clave=clave_gen, tipo_usuario='empresa')

        Empresa.objects.create(
            usuario=user,
            cedula=cedula,
            nombre_comercial=nombre_comercial,
            actividad_economica=actividad_obj,
            tipo_persona=tipo_persona,
            razon_social=razon,
            correo=correo,
            provincia=provincia,
            ciudad=ciudad,
            calle=calle,
            celular=celular
        )

        send_mail(
            'Registro exitoso - Sistema de Empleo',
            f'Bienvenido {nombre_comercial}, tus credenciales son:\nUsuario: {usuario_gen}\nContraseña: {clave_gen}',
            'tucorreo@gmail.com',
            [correo],
            fail_silently=False,
        )

        return redirect('login_empresa')

    return render(request, 'empresa/registro_empresa.html', {'actividades': actividades})

# Inicio buscador
def inicio_buscador(request):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='buscador')
        buscador = Buscador.objects.get(usuario=usuario)
        solicitudes = Solicitarempleo.objects.filter(buscador=buscador)
        empleos = Publicarempleo.objects.filter(esta_activa=True).order_by('-fecha_publicacion')

        total = solicitudes.count()
        activas = solicitudes.filter(esta_activa=True).count()
        inactivas = solicitudes.filter(esta_activa=False).count()

        context = {
            'usuario': usuario,
            'solicitudes': solicitudes,
            'empleos': empleos, 
            'total': total,
            'activas': activas,
            'inactivas': inactivas
        }
        return render(request, 'buscador/inicio_buscador.html', context)

    except (Usuario.DoesNotExist, Buscador.DoesNotExist):
        return render(request, 'error.html', {'mensaje': 'Usuario no válido o no autorizado'})

# Inicio empresa
def inicio_empresa(request):
    usuario = None
    empleos = []
    total = activas = inactivas = 0

    if 'usuario_id' in request.session:
        try:
            usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='empresa')
            empresa = Empresa.objects.get(usuario=usuario)
            empleos = Publicarempleo.objects.filter(empresa=empresa)

            total = empleos.count()
            activas = empleos.filter(esta_activa=True).count()
            inactivas = empleos.filter(esta_activa=False).count()

        except (Usuario.DoesNotExist, Empresa.DoesNotExist):
            pass

    return render(request, 'empresa/inicio_empresa.html', {
        'usuario': usuario,
        'empleos': empleos,
        'total': total,
        'activas': activas,
        'inactivas': inactivas
    })

# CERRAR SESION
def logout_usuario(request):
    request.session.flush()
    return redirect('home')


## REGISTRAR EMPLEOS ##

def registrar_empleo(request):
    if 'usuario_id' not in request.session:
        return redirect('login_empresa')  # ← CORREGIDO AQUÍ

    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='empresa')
        empresa = Empresa.objects.get(usuario=usuario)
    except (Usuario.DoesNotExist, Empresa.DoesNotExist):
        return render(request, 'error.html', {'mensaje': 'No estás autorizado para publicar empleos.'})

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        requisitos = request.POST.get('requisitos')
        salario = request.POST.get('salario') or None
        tipo_contrato = request.POST.get('tipo_contrato')
        modalidad = request.POST.get('modalidad')
        ciudad = request.POST.get('ciudad')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')

        Publicarempleo.objects.create(
            empresa=empresa,
            titulo=titulo,
            descripcion=descripcion,
            requisitos=requisitos,
            salario=salario,
            tipo_contrato=tipo_contrato,
            modalidad=modalidad,
            ciudad=ciudad,
            fecha_publicacion=timezone.now().date(),
            fecha_vencimiento=fecha_vencimiento,
            esta_activa=True
        )
        return redirect('inicio_empresa')  # O una URL de listado que quieras

    return render(request, 'empresa/registrar_empleo.html')

def editar_empleo(request, id):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='empresa')
        empresa = Empresa.objects.get(usuario=usuario)
        empleo = Publicarempleo.objects.get(id=id, empresa=empresa)
    except (Usuario.DoesNotExist, Empresa.DoesNotExist, Publicarempleo.DoesNotExist):
        return render(request, 'error.html', {'mensaje': 'Empleo no encontrado o acceso denegado.'})

    if request.method == 'POST':
        empleo.titulo = request.POST.get('titulo')
        empleo.descripcion = request.POST.get('descripcion')
        empleo.requisitos = request.POST.get('requisitos')
        empleo.tipo_contrato = request.POST.get('tipo_contrato')
        empleo.modalidad = request.POST.get('modalidad')
        empleo.ciudad = request.POST.get('ciudad')
        empleo.fecha_vencimiento = request.POST.get('fecha_vencimiento')
        empleo.esta_activa = request.POST.get('esta_activa') == 'True'

        salario_str = request.POST.get('salario')
        if salario_str:
            try:
                empleo.salario = Decimal(salario_str.replace(',', '.'))
            except InvalidOperation:
                return render(request, 'empresa/editar_empleo.html', {
                    'empleo': empleo,
                    'error': 'El valor de salario no es válido.'
                })
        else:
            empleo.salario = None

        empleo.save()
        return redirect('inicio_empresa')

    return render(request, 'empresa/editar_empleo.html', {'empleo': empleo})

def eliminar_empleo(request, id):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='empresa')
        empresa = Empresa.objects.get(usuario=usuario)
        empleo = Publicarempleo.objects.get(id=id, empresa=empresa)
        empleo.delete()
    except (Usuario.DoesNotExist, Empresa.DoesNotExist, Publicarempleo.DoesNotExist):
        return render(request, 'error.html', {'mensaje': 'No se pudo eliminar el empleo.'})

    return redirect('inicio_empresa')

def toggle_estado_empleo(request, id):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='empresa')
        empresa = Empresa.objects.get(usuario=usuario)
        empleo = Publicarempleo.objects.get(id=id, empresa=empresa)
        empleo.esta_activa = not empleo.esta_activa
        empleo.save()
    except (Usuario.DoesNotExist, Empresa.DoesNotExist, Publicarempleo.DoesNotExist):
        return render(request, 'error.html', {'mensaje': 'No se pudo cambiar el estado del empleo.'})

    return redirect('inicio_empresa')  # O la ruta donde se muestra la tabla


## ********* BUSCADOR ******** ##

def registro_solicitud_empleo(request):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='buscador')
        buscador = Buscador.objects.get(usuario=usuario)
    except (Usuario.DoesNotExist, Buscador.DoesNotExist):
        messages.error(request, "Acceso no autorizado.")
        return redirect('login_buscador')

    if request.method == 'POST':
        cargo_deseado = request.POST.get('cargo_deseado')
        nivel_estudios = request.POST.get('nivel_estudios')
        experiencia_anios = request.POST.get('experiencia_anios')
        habilidades = request.POST.get('habilidades')
        disponibilidad = request.POST.get('disponibilidad')
        ubicacion = request.POST.get('ubicacion')
        esta_activa = True if request.POST.get('esta_activa') == 'True' else False
        cv_file = request.FILES.get('cv')

        solicitud = Solicitarempleo(
            buscador=buscador,
            cargo_deseado=cargo_deseado,
            nivel_estudios=nivel_estudios,
            experiencia_anios=experiencia_anios or 0,
            habilidades=habilidades,
            disponibilidad=disponibilidad,
            ubicacion=ubicacion,
            fecha_publicacion=datetime.date.today(),
            esta_activa=esta_activa
        )

        if cv_file:
            solicitud.cv = cv_file

        solicitud.save()
        messages.success(request, "Tu solicitud fue publicada correctamente.")
        return redirect('inicio_buscador')

    return render(request, 'buscador/registro_solicitud.html')

def editar_solicitud(request, id):
    usuario_id = request.session.get('usuario_id')
    buscador = get_object_or_404(Buscador, usuario_id=usuario_id)
    solicitud = get_object_or_404(Solicitarempleo, id=id, buscador=buscador)

    if request.method == 'POST':
        solicitud.cargo_deseado = request.POST.get('cargo_deseado')
        solicitud.nivel_estudios = request.POST.get('nivel_estudios')
        solicitud.experiencia_anios = request.POST.get('experiencia_anios')
        solicitud.habilidades = request.POST.get('habilidades')
        solicitud.disponibilidad = request.POST.get('disponibilidad')
        solicitud.ubicacion = request.POST.get('ubicacion')
        solicitud.esta_activa = request.POST.get('esta_activa') == 'True'
        solicitud.fecha_publicacion = date.today()

        if request.FILES.get('cv'):
            cv_file = request.FILES['cv']
            solicitud.cv.save(cv_file.name, cv_file, save=True)

        solicitud.save()
        return redirect('inicio_buscador')

    return render(request, 'buscador/editar_solicitud.html', {'solicitud': solicitud})

def eliminar_solicitud(request, id):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='buscador')
        buscador = Buscador.objects.get(usuario=usuario)
        solicitud = Solicitarempleo.objects.get(id=id, buscador=buscador)
        solicitud.delete()
    except (Usuario.DoesNotExist, Buscador.DoesNotExist, Solicitarempleo.DoesNotExist):
        return render(request, 'error.html', {'mensaje': 'No se pudo eliminar la solicitud.'})

    return redirect('inicio_buscador')

## NOTIFICACIONES ##

def aplicar_empleo(request, empleo_id):
    try:
        usuario_id = request.session.get('usuario_id')
        usuario = Usuario.objects.get(id=usuario_id, tipo_usuario='buscador')
        buscador = Buscador.objects.get(usuario=usuario)
        empleo = Publicarempleo.objects.get(id=empleo_id)

        # Obtener la solicitud activa más reciente del buscador
        solicitud = Solicitarempleo.objects.filter(buscador=buscador, esta_activa=True).order_by('-fecha_publicacion').first()

        if Notificacion.objects.filter(buscador=buscador, empleo=empleo).exists():
            messages.info(request, 'Ya aplicaste a esta oferta anteriormente.')
        else:
            Notificacion.objects.create(
                buscador=buscador,
                empleo=empleo,
                solicitud=solicitud,
                fecha_aplicacion=timezone.now(),
                leido=False,
                mensaje=f"{buscador.nombre} ha aplicado al empleo '{empleo.titulo}'"
            )
            messages.success(request, 'Has aplicado exitosamente.')

    except (Usuario.DoesNotExist, Buscador.DoesNotExist, Publicarempleo.DoesNotExist):
        messages.error(request, 'No se pudo procesar la aplicación.')

    return redirect('inicio_buscador')

# NOTIFICACION EMPRESA
def notificaciones_empresa(request):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='empresa')
        empresa = Empresa.objects.get(usuario=usuario)

        # Obtener todos los empleos de esta empresa
        empleos = Publicarempleo.objects.filter(empresa=empresa)

        # Obtener notificaciones relacionadas con esos empleos
        notificaciones = Notificacion.objects.filter(
            empleo__in=empleos
        ).select_related('buscador', 'empleo', 'solicitud').order_by('-fecha_aplicacion')

        return render(request, 'empresa/notificaciones.html', {
            'usuario': usuario,
            'notificaciones': notificaciones
        })

    except (Usuario.DoesNotExist, Empresa.DoesNotExist):
        return render(request, 'error.html', {'mensaje': 'Acceso no autorizado'})

def responder_solicitud(request, notificacion_id, accion):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='empresa')
        notificacion = Notificacion.objects.get(id=notificacion_id, empleo__empresa__usuario=usuario)

        if accion == 'aceptar':
            notificacion.respuesta = 'aceptada'
        elif accion == 'rechazar':
            notificacion.respuesta = 'rechazada'
        notificacion.leido = False  # para que el buscador lo vea como nuevo
        notificacion.save()
        messages.success(request, f'Solicitud {accion} correctamente.')
    except Notificacion.DoesNotExist:
        messages.error(request, 'No se pudo procesar la solicitud.')

    return redirect('notificaciones_empresa')


## NOTIFICACIONES BUSCADOR ##

def notificaciones_buscador(request):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='buscador')
        buscador = Buscador.objects.get(usuario=usuario)

        notificaciones = Notificacion.objects.filter(buscador=buscador).select_related('empleo').order_by('-fecha_aplicacion')

        return render(request, 'buscador/notificaciones.html', {
            'notificaciones': notificaciones
        })
    except (Usuario.DoesNotExist, Buscador.DoesNotExist):
        return render(request, 'error.html', {'mensaje': 'Acceso no autorizado'})

## PERIFL BUSCADOR ##

def editar_perfil_buscador(request):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='buscador')
        buscador = Buscador.objects.get(usuario=usuario)
        perfil, _ = Perfilbuscador.objects.get_or_create(buscador=buscador)
    except (Usuario.DoesNotExist, Buscador.DoesNotExist):
        return render(request, 'error.html', {'mensaje': 'Acceso no autorizado'})

    if request.method == 'POST':
        perfil.biografia = request.POST.get('biografia')
        perfil.habilidades_destacadas = request.POST.get('habilidades_destacadas')
        perfil.portafolio_web = request.POST.get('portafolio_web')

        if 'foto' in request.FILES:
            perfil.foto = request.FILES['foto']  

        perfil.save()
        messages.success(request, "Perfil actualizado correctamente.")
        return redirect('ver_perfil_buscador')

    return render(request, 'buscador/perfil_extendido.html', {'perfil': perfil})


def ver_perfil_buscador(request):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='buscador')
        buscador = Buscador.objects.get(usuario=usuario)
        perfil = Perfilbuscador.objects.filter(buscador=buscador).first()
    except (Usuario.DoesNotExist, Buscador.DoesNotExist):
        return render(request, 'error.html', {'mensaje': 'Acceso no autorizado'})

    return render(request, 'buscador/ver_perfil.html', {'buscador': buscador, 'perfil': perfil})


## PERFIL EMPRESA ##

def editar_perfil_empresa(request):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='empresa')
        empresa = Empresa.objects.get(usuario=usuario)
        perfil, _ = Perfilempresa.objects.get_or_create(empresa=empresa)
    except (Usuario.DoesNotExist, Empresa.DoesNotExist):
        return render(request, 'error.html', {'mensaje': 'Acceso no autorizado'})

    if request.method == 'POST':
        perfil.descripcion = request.POST.get('descripcion')
        perfil.sitio_web = request.POST.get('sitio_web')
        perfil.facebook = request.POST.get('facebook')
        perfil.linkedin = request.POST.get('linkedin')

        if 'logo' in request.FILES:
            perfil.logo = request.FILES['logo'] 

        perfil.save()
        messages.success(request, "Perfil actualizado correctamente.")
        return redirect('ver_perfil_empresa')

    return render(request, 'empresa/perfil_extendido.html', {'perfil': perfil})

def ver_perfil_empresa(request):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'], tipo_usuario='empresa')
        empresa = Empresa.objects.get(usuario=usuario)
        perfil = Perfilempresa.objects.filter(empresa=empresa).first()
    except (Usuario.DoesNotExist, Empresa.DoesNotExist):
        return render(request, 'error.html', {'mensaje': 'Acceso no autorizado'})

    return render(request, 'empresa/ver_perfil.html', {'empresa': empresa, 'perfil': perfil})

## ACTUALIZAR CREDENCIALES ##
def actualizar_credenciales(request):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        return render(request, 'error.html', {'mensaje': 'Usuario no válido'})

    if request.method == 'POST':
        nuevo_usuario = request.POST.get('usuario')
        nueva_clave = request.POST.get('clave')

        if not nuevo_usuario or not nueva_clave:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('actualizar_credenciales')

        # Verificar que el nuevo nombre de usuario no exista en otro usuario
        if Usuario.objects.filter(usuario=nuevo_usuario).exclude(id=usuario.id).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('actualizar_credenciales')

        usuario.usuario = nuevo_usuario
        usuario.clave = nueva_clave
        usuario.save()

        messages.success(request, 'Credenciales actualizadas correctamente.')

        # Redirección según tipo de usuario
        if usuario.tipo_usuario == 'empresa':
            return redirect('ver_perfil_empresa')
        else:
            return redirect('ver_perfil_buscador')

    return render(request, 'actualizar_credenciales.html', {'usuario': usuario})