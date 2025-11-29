from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from app_movil_escolar_api.serializers import *
from app_movil_escolar_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import get_object_or_404

# 1. LISTAR TODOS LOS EVENTOS
class EventosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        # Traemos todos los eventos ordenados por ID
        # OJO: En tu modelo se llama 'responsable', no 'user'
        eventos = Eventos.objects.all().order_by("id")
        
        # Si quisieras filtrar solo los activos del responsable:
        # eventos = Eventos.objects.filter(responsable__is_active=True).order_by("id")
        
        lista = EventoSerializer(eventos, many=True).data
        return Response(lista, 200)

# 2. VER (POR ID) Y CREAR NUEVO
class EventosView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    # Obtener un evento por ID
    def get(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.GET.get("id"))
        evento_json = EventoSerializer(evento)
        return Response(evento_json.data, 200)

    # Registrar nuevo evento
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # 1. Validamos que el 'responsable' exista en la BD de usuarios
        id_responsable = request.data["responsable"]
        usuario_responsable = get_object_or_404(User, id=id_responsable)

        # 2. Creamos el evento usando los datos del request
        # Osea, aquí NO creamos usuarios nuevos, solo vinculamos
        try:
            evento = Eventos.objects.create(
                responsable = usuario_responsable,
                nombre = request.data["nombre"],
                tipo = request.data["tipo"],
                fecha = request.data["fecha"],
                hora_inicio = request.data["hora_inicio"],
                hora_fin = request.data["hora_fin"],
                lugar = request.data["lugar"],
                # Checkboxes
                es_estudiantes = request.data.get("es_estudiantes", False),
                es_profesores = request.data.get("es_profesores", False),
                es_publico = request.data.get("es_publico", False),
                # Opcionales
                programa = request.data.get("programa", None),
                descripcion = request.data.get("descripcion", ""),
                cupo = request.data.get("cupo", 0)
            )
            
            evento.save()
            return Response({"message": "Evento creado exitosamente", "id": evento.id}, 201)

        except Exception as e:
            return Response({"error": str(e)}, 400)

# 3. EDITAR Y ELIMINAR
class EventosViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    # Actualizar evento
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        # Buscamos el evento
        evento = get_object_or_404(Eventos, id=request.data["id"])
        
        # Actualizamos campos
        # Nota: Si cambiaron al responsable, hay que buscar al user de nuevo
        if "responsable" in request.data:
            evento.responsable = get_object_or_404(User, id=request.data["responsable"])

        evento.nombre = request.data["nombre"]
        evento.tipo = request.data["tipo"]
        evento.fecha = request.data["fecha"]
        evento.hora_inicio = request.data["hora_inicio"]
        evento.hora_fin = request.data["hora_fin"]
        evento.lugar = request.data["lugar"]
        
        evento.es_estudiantes = request.data["es_estudiantes"]
        evento.es_profesores = request.data["es_profesores"]
        evento.es_publico = request.data["es_publico"]
        
        evento.programa = request.data.get("programa", None)
        evento.descripcion = request.data.get("descripcion", "")
        evento.cupo = request.data.get("cupo", 0)
        
        evento.save()
        
        return Response({"message": "Evento actualizado correctamente"}, 200)

    # Eliminar evento
    def delete(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.GET.get("id"))
        try:
            evento.delete()
            return Response({"message": "Evento eliminado correctamente"}, 200)
        except Exception as e:
            return Response({"message": "No se pudo eliminar el evento"}, 400)