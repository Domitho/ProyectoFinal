from django.shortcuts import render, redirect
from .models import Usuario

# Vista Login
def login_view(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        clave = request.POST['clave']

        try:
            user = Usuario.objects.get(usuario=usuario, clave=clave)

            if user.tipo_usuario == 'buscador':
                return redirect('inicio_buscador')
            elif user.tipo_usuario == 'empresa':
                return redirect('inicio_empresa')
        except Usuario.DoesNotExist:
            return render(request, 'login.html', {'error': 'Usuario o clave incorrectos'})

    return render(request, 'login.html')


# Vista Registro
def registro_view(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        clave = request.POST['clave']
        tipo_usuario = request.POST['tipo_usuario']

        if Usuario.objects.filter(usuario=usuario).exists():
            return render(request, 'registro.html', {'error': 'El usuario ya existe'})

        Usuario.objects.create(usuario=usuario, clave=clave, tipo_usuario=tipo_usuario)
        return redirect('login')

    return render(request, 'registro.html')


# Vista inicio buscador
def inicio_buscador(request):
    return render(request, 'inicio_buscador.html')


# Vista inicio empresa
def inicio_empresa(request):
    return render(request, 'inicio_empresa.html')
