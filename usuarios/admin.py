from django.contrib import admin
from .models import Juego, Usuario, Estadistica

# Registrar los modelos para que aparezcan en el admin
admin.site.register(Juego)
admin.site.register(Usuario)

@admin.register(Estadistica)
class EstadisticaAdmin(admin.ModelAdmin):
    list_filter = ('juego',)
    ordering = ('jugador', 'juego')
    def get_list_display(self, request):
        """
        Cambia las columnas según el juego seleccionado en la vista.
        """
        # Aqui usamos request.GET para filtrar por juego
        juego_id = request.GET.get('juego__id__exact')

        if juego_id in ['2', '3']:
            return ('jugador', 'juego', 'kills')
        else:
            return ('jugador', 'juego', 'partidos_ganados', 'goles')


