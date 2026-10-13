import json
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Pelicula

# Create your views here.
# Validar la información de una pelicula
def validar_datos(datos):
    titulo = datos["titulo"]
    genero = datos["genero"]
    anio = datos["anio"]
    calificacion = Decimal(str(datos["calificacion"]))
    
    if not isinstance(titulo, str) or not titulo.strip():
        raise ValueError("El título es obligatorio")
    
    if not isinstance(genero, str) or not genero.strip():
        raise ValueError("El género es obligatorio")

    if isinstance(anio, bool) or not isinstance(anio, int):
        raise ValueError("El año debe ser entero")
    
    if anio < 1900:
        raise ValueError("Año inválido")
    
    if not calificacion.is_finite() or not 0 <= calificacion <= 10:
        raise ValueError("La calificación debe estar entre 0 y 10")
    
    return titulo.strip(), genero.strip(), anio, calificacion

# GET: MOSTRAR INFORMACIÓN (PELÍCULAS)
# POST: AGREGAR INFORMACIÓN (PELÍCULAS)
@csrf_exempt
def peliculas(request):
    
    if request.method == 'GET':
        
        lista = list(
            Pelicula.objects.values()
        )
        
        return JsonResponse({
            "peliculas": lista
        })
        
    elif request.method == 'POST':
        
        try:
            datos = json.loads(request.body)
            
            titulo, genero, anio, calificacion = validar_datos(datos)
            
            pelicula = Pelicula.objects.create(
                titulo=titulo,
                genero=genero,
                anio=anio,
                calificacion=calificacion
            )
            
            return JsonResponse({
                "mensaje": "Película registrada correctamente",
                "id": pelicula.id
            }, status=201)
            
        except (
            ValueError,
            KeyError,
            TypeError,
            InvalidOperation,
            json.JSONDecodeError
        ):
            return JsonResponse({
                "error": "Datos inválidos"
            }, status=400)
    
    return JsonResponse({
        "error": "Método no permitido"
    }, status=405)    
    
# PUT: ACTUALIZAR INFORMACIÓN (PELÍCULAS)
@csrf_exempt        
def actualizar_peliculas(request, pelicula_id):
    
    if request.method != 'PUT':
        
        return JsonResponse({
            "error": "Método no permitido"
        }, status=405)
    
    try: 
        pelicula = Pelicula.objects.get(
            id=pelicula_id
        )
        
    except Pelicula.DoesNotExist:
        
        return JsonResponse({
            "error": "Película no encontrada"
        }, status=404)
    
    try:
        datos = json.loads(request.body)  
        
        titulo, genero, anio, calificacion = validar_datos(datos)   
        
    except (
        ValueError,
        KeyError,
        TypeError,
        InvalidOperation,
        json.JSONDecodeError
    ):
        return JsonResponse({
            "error": "Datos inválidos"
        }, status=400)
        
    pelicula.titulo = titulo
    pelicula.genero = genero
    pelicula.anio = anio
    pelicula.calificacion = calificacion
    
    pelicula.save()    
          
    return JsonResponse({
        "mensaje": "Película actualizada correctamente"
    })
    
# VISTA PARA MOSTRTAR HTML
def inicio(request):
    
    lista_peliculas = Pelicula.objects.all()
    
    return render(
        request,
        'peliculas/index.html',
        {'peliculas': lista_peliculas}
    )