from django.shortcuts import render, redirect
from .models import Usuario, Buscador, Empresa
from django.core.mail import send_mail


# Pantalla de inicio
def home(request):
    return render(request, 'home.html')

# Login buscador
def login_buscador(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        clave = request.POST['clave']

        try:
            user = Usuario.objects.get(usuario=usuario, clave=clave, tipo_usuario='buscador')
            return redirect('inicio_buscador')
        except Usuario.DoesNotExist:
            return render(request, 'login_buscador.html', {'error': 'Usuario o clave incorrectos'})

    return render(request, 'login_buscador.html')

# Login empresa
def login_empresa(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        clave = request.POST['clave']

        try:
            user = Usuario.objects.get(usuario=usuario, clave=clave, tipo_usuario='empresa')
            return redirect('inicio_empresa')
        except Usuario.DoesNotExist:
            return render(request, 'login_empresa.html', {'error': 'Usuario o clave incorrectos'})

    return render(request, 'login_empresa.html')



def registro_buscador(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        clave = request.POST['clave']
        cedula = request.POST['cedula']
        apellido = request.POST['apellido']
        fecha = request.POST['fecha']
        genero = request.POST['genero']
        correo = request.POST['correo']

        if Usuario.objects.filter(usuario=usuario).exists():
            return render(request, 'registro_buscador.html', {'error': 'El usuario ya existe'})

        user = Usuario.objects.create(usuario=usuario, clave=clave, tipo_usuario='buscador')

        Buscador.objects.create(
            usuario=user,
            cedula=cedula,
            apellido=apellido,
            fecha_nacimiento=fecha,
            genero=genero,
            correo=correo
        )

        # Enviar correo
        send_mail(
            'Registro exitoso en Sistema de Empleo',
            f'Bienvenido {usuario}, tus credenciales son:\nUsuario: {usuario}\nContraseña: {clave}',
            'tucorreo@gmail.com',
            [correo],
            fail_silently=False,
        )

        return redirect('login_buscador')

    return render(request, 'registro_buscador.html')

from .models import Usuario, Empresa

def registro_empresa(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        clave = request.POST['clave']
        nombre = request.POST['nombre']
        actividad = request.POST['actividad']
        razon = request.POST['razon']
        correo = request.POST['correo']

        if Usuario.objects.filter(usuario=usuario).exists():
            return render(request, 'registro_empresa.html', {'error': 'El usuario ya existe'})

        user = Usuario.objects.create(usuario=usuario, clave=clave, tipo_usuario='empresa')

        Empresa.objects.create(
            usuario=user,
            nombre_comercial=nombre,
            actividad_economica=actividad,
            razon_social=razon,
            correo=correo
        )

        # Enviar correo
        send_mail(
            'Registro exitoso en Sistema de Empleo',
            f'Bienvenido {usuario}, tus credenciales son:\nUsuario: {usuario}\nContraseña: {clave}',
            'tucorreo@gmail.com',
            [correo],
            fail_silently=False,
        )

        return redirect('login_empresa')

    return render(request, 'registro_empresa.html')

def inicio_buscador(request):
    return render(request, 'inicio_buscador.html')

# Inicio empresa
def inicio_empresa(request):
    return render(request, 'inicio_empresa.html')
