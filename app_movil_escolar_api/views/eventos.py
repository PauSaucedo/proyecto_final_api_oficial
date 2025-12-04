from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from app_movil_escolar_api.serializers import EventoSerializer
from app_movil_escolar_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class EventosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        eventos = Eventos.objects.all().order_by("id")
        lista = EventoSerializer(eventos, many=True).data
        return Response(lista, 200)

class EventosView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.query_params.get('id'))
        serializer = EventoSerializer(evento)
        return Response(serializer.data, 200)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            id_responsable = request.data["responsable"]
            usuario_responsable = get_object_or_404(User, id=id_responsable)

            evento = Eventos.objects.create(
                responsable=usuario_responsable,
                nombre=request.data["nombre"],
                tipo=request.data["tipo"],
                fecha=request.data["fecha"],
                hora_inicio=request.data["hora_inicio"],
                hora_fin=request.data["hora_fin"],
                lugar=request.data["lugar"],
                es_estudiantes=request.data["es_estudiantes", False],
                es_profesores=request.data["es_profesores", False],
                es_publico=request.data["es_publico", False],
                programa=request.data["programa", None],
                descripcion=request.data["descripcion", ""],
                cupo=request.data["cupo", 0]
            )
            
            evento.save()
            return Response({"message": "Evento creado exitosamente", "id": evento.id}, 201)
        except Exception as e:
            return Response({"error": str(e)}, 400)

class EventosViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.data["id"])
        
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

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.GET.get("id"))
        try:
            evento.delete()
            return Response({"message": "Evento eliminado correctamente"}, 200)
        except Exception as e:
            return Response({"message": "No se pudo eliminar el evento"}, 400)