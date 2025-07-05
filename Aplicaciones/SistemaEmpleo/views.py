from django.shortcuts import render, redirect
from .models import Usuario

# Página de inicio pública
def home(request):
    return render(request, 'home.html')

# Login para buscadores
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

# Login para empresas
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

# Registro
def registro_view(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        clave = request.POST['clave']
        tipo_usuario = request.POST['tipo_usuario']

        if Usuario.objects.filter(usuario=usuario).exists():
            return render(request, 'registro.html', {'error': 'El usuario ya existe'})

        Usuario.objects.create(usuario=usuario, clave=clave, tipo_usuario=tipo_usuario)
        return redirect('home')

    return render(request, 'registro.html')

# Inicio buscador
def inicio_buscador(request):
    return render(request, 'inicio_buscador.html')

# Inicio empresa
def inicio_empresa(request):
    return render(request, 'inicio_empresa.html')
