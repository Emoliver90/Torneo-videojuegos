from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import RegistroForm
from .models import Juego, Estadistica


def index(request):
    """Página de bienvenida con los accesos a registro, login y ranking."""
    return render(request, 'index.html')


def registro(request):
    """Registro de un nuevo usuario del torneo."""
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('perfil')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


@login_required
def perfil(request):
    """Perfil del usuario autenticado con su estadística en el juego actual."""
    user = request.user
    if user.is_superuser:
        return redirect('/admin/')

    estadistica = user.estadistica_set.filter(juego=user.juego).first()

    return render(request, 'perfil.html', {
        'estadistica': estadistica,
    })


def obtener_ranking(juego):
    """Devuelve el queryset de Estadistica ordenado según el tipo de ranking del juego."""
    if juego.tipo_ranking == 'kills':
        return Estadistica.objects.filter(juego=juego).select_related('jugador', 'juego').order_by('-kills')

    if juego.tipo_ranking == 'wins_goals':
        return (
            Estadistica.objects.filter(juego=juego)
            .select_related('jugador', 'juego')
            .order_by('-partidos_ganados', '-goles')
        )

    return Estadistica.objects.none()


def estadisticas(request):
    """Ranking general o filtrado por juego, con los datos para la gráfica."""
    juego_id = request.GET.get('juego')
    juegos = Juego.objects.all()

    if juego_id:
        juego = get_object_or_404(Juego, id=juego_id)
        estadisticas_qs = obtener_ranking(juego)
        tipo_ranking = juego.tipo_ranking
    else:
        estadisticas_qs = (
            Estadistica.objects.select_related('jugador', 'juego')
            .order_by('jugador__username', 'juego__nombre')
        )
        tipo_ranking = 'all'

    # Datos para la gráfica: según el tipo de ranking se usa una métrica u otra.
    if tipo_ranking == 'kills':
        puntos = [e.kills for e in estadisticas_qs]
    elif tipo_ranking == 'wins_goals':
        puntos = [e.partidos_ganados for e in estadisticas_qs]
    else:  # 'all': se muestra un total combinado a modo orientativo
        puntos = [e.kills + e.partidos_ganados + e.goles for e in estadisticas_qs]

    nombres = [e.jugador.username for e in estadisticas_qs]

    return render(request, 'estadisticas.html', {
        'estadisticas': estadisticas_qs,
        'juegos': juegos,
        'juego_id': juego_id,
        'tipo_ranking': tipo_ranking,
        'nombres': nombres,
        'puntos': puntos,
    })
