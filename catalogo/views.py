from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import CustomUser, Libro, Materia, Mensaje, ContactoMensaje
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, LibroForm,
    MensajeForm, RespuestaMensajeForm, PerfilForm, CambioPasswordForm,
    ContactoForm,
)


def index(request):
    total_usuarios = CustomUser.objects.count()
    total_libros = Libro.objects.count()
    return render(request, 'index.html', {
        'total_usuarios': total_usuarios,
        'total_libros': total_libros,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalogo')
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalogo')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('catalogo')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalogo')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def catalogo_view(request):
    libros = Libro.objects.select_related('usuario', 'materia').all()
    # No se usan favoritos en esta vista
    favoritos_ids = []
    return render(request, 'catalogo.html', {
        'libros': libros,
        'favoritos_ids': favoritos_ids,
        'active': 'catalogo',
    })


@login_required
def publicar_view(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            libro = form.save(commit=False)
            libro.usuario = request.user
            libro.save()
            messages.success(request, '¡Libro publicado con éxito!')
            return redirect('catalogo')
    else:
        form = LibroForm()
    return render(request, 'publicar.html', {
        'form': form,
        'active': 'publicar',
    })


@login_required
def perfil_view(request):
    mis_libros = Libro.objects.filter(usuario=request.user)
    disponibles = mis_libros.filter(estado='disponible').count()
    prestados = mis_libros.filter(estado='prestado').count()
    donados = mis_libros.filter(estado='donado').count()
    return render(request, 'perfil.html', {
        'mis_libros': mis_libros,
        'disponibles': disponibles,
        'prestados': prestados,
        'donados': donados,
        'active': 'perfil',
    })


@login_required
def solicitar_view(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    dueno = libro.usuario
    if dueno == request.user:
        messages.warning(request, 'No puedes solicitar tu propio libro.')
        return redirect('catalogo')
    return render(request, 'solicitar.html', {
        'libro': libro, 'dueno': dueno, 'active': 'catalogo',
    })


@login_required
def eliminar_libro_view(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id, usuario=request.user)
    titulo = libro.titulo
    libro.delete()
    messages.success(request, f'Libro "{titulo}" eliminado.')
    return redirect('perfil')


# ─── MATERIAS ─────────────────────────────────────

def materias_lista(request):
    materias = Materia.objects.annotate(
        total_libros=Count('libros', filter=Q(libros__estado='disponible'))
    )
    return render(request, 'materias/lista.html', {
        'materias': materias,
        'active': 'materias',
    })


def materias_libros(request, slug):
    materia = get_object_or_404(Materia, slug=slug)
    libros = Libro.objects.filter(materia=materia).select_related('usuario')
    return render(request, 'materias/libros.html', {
        'materia': materia,
        'libros': libros,
        'active': 'materias',
    })


# ─── MENSAJES ─────────────────────────────────────

@login_required
def mensajes_inbox(request):
    mensajes = Mensaje.objects.filter(destinatario=request.user).select_related('remitente', 'libro')
    no_leidos = mensajes.filter(leido=False).count()
    return render(request, 'mensajes/inbox.html', {
        'mensajes': mensajes,
        'no_leidos': no_leidos,
        'active': 'mensajes',
    })


@login_required
def mensajes_enviados(request):
    mensajes = Mensaje.objects.filter(remitente=request.user).select_related('destinatario', 'libro')
    return render(request, 'mensajes/enviados.html', {
        'mensajes': mensajes,
        'active': 'mensajes',
    })


@login_required
def mensajes_enviar(request, libro_id=None):
    libro = None
    if libro_id:
        libro = get_object_or_404(Libro, id=libro_id)

    initial = {}
    if libro:
        initial['destinatario'] = libro.usuario_id

    if request.method == 'POST':
        form = MensajeForm(request.POST, initial=initial, remitente=request.user)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            if libro:
                mensaje.libro = libro
            mensaje.save()
            messages.success(request, 'Mensaje enviado correctamente.')
            return redirect('mensajes_inbox')
    else:
        form = MensajeForm(initial=initial, remitente=request.user)

    return render(request, 'mensajes/enviar.html', {
        'form': form,
        'libro': libro,
        'active': 'mensajes',
    })


@login_required
def mensajes_hilo(request, mensaje_id):
    mensaje = get_object_or_404(Mensaje, id=mensaje_id)

    if request.user not in (mensaje.remitente, mensaje.destinatario):
        messages.error(request, 'No tienes permiso para ver este mensaje.')
        return redirect('mensajes_inbox')

    if mensaje.destinatario == request.user and not mensaje.leido:
        mensaje.leido = True
        mensaje.save(update_fields=['leido'])

    # Obtener todo el hilo (mensajes entre los mismos usuarios sobre el mismo libro)
    hilo = Mensaje.objects.filter(
        Q(remitente=mensaje.remitente, destinatario=mensaje.destinatario) |
        Q(remitente=mensaje.destinatario, destinatario=mensaje.remitente),
        libro=mensaje.libro,
    ).order_by('fecha_envio').select_related('remitente', 'destinatario')

    if request.method == 'POST':
        form = RespuestaMensajeForm(request.POST)
        if form.is_valid():
            Mensaje.objects.create(
                remitente=request.user,
                destinatario=mensaje.remitente if request.user == mensaje.destinatario else mensaje.destinatario,
                libro=mensaje.libro,
                contenido=form.cleaned_data['contenido'],
            )
            messages.success(request, 'Respuesta enviada.')
            return redirect('mensajes_hilo', mensaje_id=mensaje_id)
    else:
        form = RespuestaMensajeForm()

    otro_usuario = mensaje.destinatario if request.user == mensaje.remitente else mensaje.remitente

    return render(request, 'mensajes/hilo.html', {
        'mensajes_hilo': hilo,
        'form': form,
        'otro_usuario': otro_usuario,
        'libro': mensaje.libro,
        'active': 'mensajes',
    })


# ─── AJUSTES ─────────────────────────────────────

@login_required
def ajustes_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('ajustes_perfil')
    else:
        form = PerfilForm(instance=request.user)
    return render(request, 'ajustes/perfil.html', {
        'form': form,
        'active': 'perfil',
    })


@login_required
def ajustes_password(request):
    if request.method == 'POST':
        form = CambioPasswordForm(request.POST)
        if form.is_valid():
            if not request.user.check_password(form.cleaned_data['password_actual']):
                form.add_error('password_actual', 'Contraseña actual incorrecta.')
            elif form.cleaned_data['nueva_password'] != form.cleaned_data['confirmar_password']:
                form.add_error('confirmar_password', 'Las contraseñas no coinciden.')
            else:
                request.user.set_password(form.cleaned_data['nueva_password'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Contraseña cambiada correctamente.')
                return redirect('ajustes_perfil')
    else:
        form = CambioPasswordForm()
    return render(request, 'ajustes/password.html', {
        'form': form,
        'active': 'perfil',
    })


# ─── PÁGINAS ESTÁTICAS ─────────────────────────────

def pagina_acerca(request):
    total_usuarios = CustomUser.objects.count()
    total_libros = Libro.objects.count()
    return render(request, 'paginas/acerca.html', {
        'total_usuarios': total_usuarios,
        'total_libros': total_libros,
    })


def pagina_faq(request):
    return render(request, 'paginas/faq.html')


def pagina_terminos(request):
    return render(request, 'paginas/terminos.html')


def pagina_contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensaje enviado. Te responderemos pronto.')
            return redirect('pagina_contacto')
    else:
        form = ContactoForm()
    return render(request, 'paginas/contacto.html', {'form': form})


# ─── MAPA DE INTERCAMBIO ────────────────────────

@login_required
def mapa_intercambio(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    propietario = libro.usuario
    solicitante = request.user
    # Preparar datos para el template
    data = {
        'solicitante': {
            'name': solicitante.nombre,
            'lat': float(solicitante.latitude) if solicitante.latitude else None,
            'lng': float(solicitante.longitude) if solicitante.longitude else None,
        },
        'propietario': {
            'name': propietario.nombre,
            'lat': float(propietario.latitude) if propietario.latitude else None,
            'lng': float(propietario.longitude) if propietario.longitude else None,
        },
    }
    return render(request, 'catalogo/mapa.html', {
        'libro': libro,
        'solicitante': solicitante,
        'propietario': propietario,
        'MAP_DATA': data,
    })
