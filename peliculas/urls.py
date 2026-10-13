from django.urls import path
from . import views

urlpatterns = [
    
    path(
        'peliculas/',
        views.peliculas,
        name='peliculas'
    ),
    
    path(
        'peliculas/<int:pelicula_id>/',
        views.actualizar_peliculas,
        name='actualizar_peliculas'
    ),
    
]