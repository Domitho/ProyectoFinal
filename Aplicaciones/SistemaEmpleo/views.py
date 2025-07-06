from django.shortcuts import render, redirect
from .models import Usuario

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

# Registro buscador
def registro_buscador(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        clave = request.POST['clave']

        if Usuario.objects.filter(usuario=usuario).exists():
            return render(request, 'registro_buscador.html', {'error': 'El usuario ya existe'})

        Usuario.objects.create(usuario=usuario, clave=clave, tipo_usuario='buscador')
        return redirect('login_buscador')

    return render(request, 'registro_buscador.html')

# Registro empresa
def registro_empresa(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        clave = request.POST['clave']

        if Usuario.objects.filter(usuario=usuario).exists():
            return render(request, 'registro_empresa.html', {'error': 'El usuario ya existe'})

        Usuario.objects.create(usuario=usuario, clave=clave, tipo_usuario='empresa')
        return redirect('login_empresa')

    return render(request, 'registro_empresa.html')

# Inicio buscador
def inicio_buscador(request):
    return render(request, 'inicio_buscador.html')

# Inicio empresa
def inicio_empresa(request):
    return render(request, 'inicio_empresa.html')
