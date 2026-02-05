from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Count, Q
from datetime import date
from .models import PerfilArmy, FotoGaleria, ListaPersonal
from .forms import PerfilArmyForm, FotoGaleriaForm, ListaPersonalForm, RegistroForm


# Vista principal - Directorio de todos los ARMY
def directorio_army(request):
    perfiles = PerfilArmy.objects.all().select_related('usuario')
    
    # Estadísticas
    total_miembros = perfiles.count()
    estadisticas_genero = perfiles.values('genero').annotate(total=Count('genero'))
    
    # Calcular edades
    edades = []
    for perfil in perfiles:
        if perfil.fecha_nacimiento:
            edad = perfil.edad()
            if edad:
                edades.append(edad)
    
    # Rangos de edad
    rango_menor_18 = len([e for e in edades if e < 18])
    rango_18_25 = len([e for e in edades if 18 <= e <= 25])
    rango_26_35 = len([e for e in edades if 26 <= e <= 35])
    rango_mayor_35 = len([e for e in edades if e > 35])
    
    # Contar por género
    masculino = perfiles.filter(genero='M').count()
    femenino = perfiles.filter(genero='F').count()
    otro = perfiles.filter(genero='O').count()
    no_especificado = perfiles.filter(Q(genero='N') | Q(genero='')).count()
    
    context = {
        'perfiles': perfiles,
        'total_miembros': total_miembros,
        'masculino': masculino,
        'femenino': femenino,
        'otro': otro,
        'no_especificado': no_especificado,
        'rango_menor_18': rango_menor_18,
        'rango_18_25': rango_18_25,
        'rango_26_35': rango_26_35,
        'rango_mayor_35': rango_mayor_35,
    }
    
    return render(request, 'directorio.html', context)


# Ver perfil de un miembro
def ver_perfil(request, username):
    perfil = get_object_or_404(PerfilArmy, usuario__username=username)
    fotos = perfil.galeria.all()
    listas = perfil.listas.all()
    
    context = {
        'perfil': perfil,
        'fotos': fotos,
        'listas': listas,
        'es_propio': request.user.is_authenticated and request.user == perfil.usuario
    }
    
    return render(request, 'ver_perfil.html', context)


# Editar propio perfil
@login_required
def editar_perfil(request):
    try:
        perfil = request.user.perfil_army
    except PerfilArmy.DoesNotExist:
        perfil = PerfilArmy.objects.create(usuario=request.user, nombre=request.user.username)
    
    if request.method == 'POST':
        form = PerfilArmyForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Perfil actualizado exitosamente! 💜')
            return redirect('ver_perfil', username=request.user.username)
    else:
        form = PerfilArmyForm(instance=perfil)
    
    return render(request, 'editar_perfil.html', {'form': form})


# Subir foto a galería
@login_required
def subir_foto(request):
    try:
        perfil = request.user.perfil_army
    except PerfilArmy.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil primero.')
        return redirect('editar_perfil')
    
    if request.method == 'POST':
        form = FotoGaleriaForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.perfil = perfil
            foto.save()
            messages.success(request, '¡Foto subida exitosamente! 📸')
            return redirect('ver_perfil', username=request.user.username)
    else:
        form = FotoGaleriaForm()
    
    return render(request, 'subir_foto.html', {'form': form})


# Eliminar foto
@login_required
def eliminar_foto(request, foto_id):
    foto = get_object_or_404(FotoGaleria, id=foto_id)
    
    # Verificar que la foto pertenece al usuario
    if foto.perfil.usuario != request.user:
        messages.error(request, 'No puedes eliminar fotos de otros usuarios.')
        return redirect('directorio_army')
    
    if request.method == 'POST':
        foto.delete()
        messages.success(request, 'Foto eliminada exitosamente.')
        return redirect('ver_perfil', username=request.user.username)
    
    return render(request, 'confirmar_eliminar_foto.html', {'foto': foto})


# Crear lista personal
@login_required
def crear_lista(request):
    try:
        perfil = request.user.perfil_army
    except PerfilArmy.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil primero.')
        return redirect('editar_perfil')
    
    if request.method == 'POST':
        form = ListaPersonalForm(request.POST)
        if form.is_valid():
            lista = form.save(commit=False)
            lista.perfil = perfil
            lista.save()
            messages.success(request, '¡Lista creada exitosamente! 📝')
            return redirect('ver_perfil', username=request.user.username)
    else:
        form = ListaPersonalForm()
    
    return render(request, 'crear_lista.html', {'form': form})


# Editar lista
@login_required
def editar_lista(request, lista_id):
    lista = get_object_or_404(ListaPersonal, id=lista_id)
    
    # Verificar que la lista pertenece al usuario
    if lista.perfil.usuario != request.user:
        messages.error(request, 'No puedes editar listas de otros usuarios.')
        return redirect('directorio_army')
    
    if request.method == 'POST':
        form = ListaPersonalForm(request.POST, instance=lista)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Lista actualizada exitosamente!')
            return redirect('ver_perfil', username=request.user.username)
    else:
        form = ListaPersonalForm(instance=lista)
    
    return render(request, 'editar_lista.html', {'form': form, 'lista': lista})


# Eliminar lista
@login_required
def eliminar_lista(request, lista_id):
    lista = get_object_or_404(ListaPersonal, id=lista_id)
    
    # Verificar que la lista pertenece al usuario
    if lista.perfil.usuario != request.user:
        messages.error(request, 'No puedes eliminar listas de otros usuarios.')
        return redirect('directorio_army')
    
    if request.method == 'POST':
        lista.delete()
        messages.success(request, 'Lista eliminada exitosamente.')
        return redirect('ver_perfil', username=request.user.username)
    
    return render(request, 'confirmar_eliminar_lista.html', {'lista': lista})


# Registro de usuario
def registro(request):
    if request.user.is_authenticated:
        return redirect('directorio_army')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear perfil automáticamente
            PerfilArmy.objects.create(usuario=user, nombre=user.username)
            login(request, user)
            messages.success(request, f'¡Bienvenido/a al sistema ARMY, {user.username}! 💜 Completa tu perfil.')
            return redirect('editar_perfil')
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})


# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('directorio_army')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido/a de vuelta, {username}! 💜')
                return redirect('directorio_army')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


# Logout
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, '¡Hasta pronto! 💜')
    return redirect('login')