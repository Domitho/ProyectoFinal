from decimal import Decimal, InvalidOperation
import random
import string
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from .models import Usuario, Buscador, Empresa, ActividadEconomica, Publicarempleo, Solicitarempleo
from django.utils import timezone
import datetime
from django.contrib import messages
from datetime import date

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

    return render(request, 'login_buscador.html')


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

    return render(request, 'registro_buscador.html')

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

        total = solicitudes.count()
        activas = solicitudes.filter(esta_activa=True).count()
        inactivas = solicitudes.filter(esta_activa=False).count()

        context = {
            'usuario': usuario,
            'solicitudes': solicitudes,
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

    return render(request, 'registrar_empleo.html')

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
    usuario_id = request.session.get('usuario_id')
    buscador = get_object_or_404(Buscador, usuario_id=usuario_id)
    solicitud = get_object_or_404(Solicitarempleo, id=id, buscador=buscador)

    if request.method == 'POST':
        solicitud.delete()
        return redirect('dashboard_solicitudes')

    return render(request, 'buscador/confirmar_eliminar.html', {'solicitud': solicitud})
