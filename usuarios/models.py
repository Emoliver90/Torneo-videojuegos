from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo de juego
class Juego(models.Model):
    TIPO_RANKING = (
        ('kills', 'Ranking por Kills'),
        ('wins_goals', 'Ranking por Victorias y Goles'),
    )
    nombre = models.CharField(max_length=100, unique=True)
    tipo_ranking = models.CharField(max_length=20, choices=TIPO_RANKING,default='kills')

    def __str__(self):
        return self.nombre

# Usuario personalizado
class Usuario(AbstractUser):

    NIVEL_CHOICES = [
        ('AM', 'Amateur'),
        ('NO', 'Normal'),
        ('EX', 'Expert'),
    ]

    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, null=True,blank=True)
    nivel = models.CharField(max_length=2, choices=NIVEL_CHOICES, null=True,blank=True)

    def __str__(self):
        return self.username

class Estadistica(models.Model):
    jugador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    # Para shooters
    kills = models.IntegerField(default=0)
    # Para juegos deportivos
    partidos_ganados = models.IntegerField(default=0)
    goles = models.IntegerField(default=0)
    class Meta:
        unique_together = ('jugador', 'juego')

    def __str__(self):
        return f'{self.jugador.username} - {self.juego.nombre}'

    def puntaje(self):
        """
        Devuelve el valor que se usará para el ranking
        dependiendo del tipo de juego.
        """
        if self.juego.tipo_ranking == 'kills':
            return self.kills

        elif self.juego.tipo_ranking == 'wins_goals':
            return (self.partidos_ganados * 3) + self.goles

        return 0