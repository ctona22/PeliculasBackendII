from django.db import models

# Create your models here.
class Pelicula(models.Model):
    titulo = models.CharField(max_length=150)
    genero = models.CharField(max_length=50)
    anio = models.IntegerField()
    calificacion = models.DecimalField(
        max_digits=3,
        decimal_places=1
    )
    
    imagen = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )
    
    def __str__(self):
        return self.titulo