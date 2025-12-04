from django.db.models import *
from django.db import transaction
from app_movil_escolar_api.serializers import UserSerializer, MaestroSerializer
from app_movil_escolar_api.models import *
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from django.contrib.auth.models import Group
import json
from django.shortcuts import get_object_or_404

class MaestrosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        maestros = Maestros.objects.filter(user__is_active=1).order_by("id")
        # Eliminamos el loop manual, devolvemos serializado directo
        lista = MaestroSerializer(maestros, many=True).data
        return Response(lista, 200)

class MaestrosView(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        maestro = get_object_or_404(Maestros, id=request.query_params.get('id'))
        # Preparamos datos para editar, igual que antes pero más limpio
        serializer = MaestroSerializer(maestro)
        data = dict(serializer.data)
        # Aplanado básico para el front si es necesario, o dejar que el front lo haga
        # Aquí mantenemos la estructura de serializador para consistencia
        return Response(data, 200)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            role = request.data['rol']
            # ... (creación de usuario igual) ...
            email = request.data['email']
            if User.objects.filter(email=email).exists():
                return Response({"message": "Username taken"}, 400)
            
            user = User.objects.create(username=email, email=email, first_name=request.data['first_name'], last_name=request.data['last_name'], is_active=1)
            user.set_password(request.data['password'])
            user.save()
            
            group, _ = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()
            
            maestro = Maestros.objects.create(
                user=user,
                id_trabajador=request.data["id_trabajador"],
                fecha_nacimiento=request.data["fecha_nacimiento"],
                telefono=request.data["telefono"],
                rfc=request.data["rfc"].upper(),
                cubiculo=request.data["cubiculo"],
                area_investigacion=request.data["area_investigacion"],
                materias_json=json.dumps(request.data["materias_json"])
            )
            maestro.save()
            return Response({"Maestro creado con ID": maestro.id}, 201)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

class MaestrosViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        maestro = get_object_or_404(Maestros, id=request.data["id"])
        maestro.id_trabajador = request.data["id_trabajador"]
        maestro.telefono = request.data["telefono"]
        maestro.rfc = request.data["rfc"]
        maestro.cubiculo = request.data["cubiculo"]
        maestro.area_investigacion = request.data["area_investigacion"]
        maestro.materias_json = json.dumps(request.data["materias_json"])
        maestro.save()
        
        user = maestro.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()
        
        return Response({"message": "Maestro actualizado"}, 200)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        maestro = get_object_or_404(Maestros, id=request.GET.get("id"))
        try:
            maestro.user.delete()
            return Response({"message": "Maestro eliminado"}, 200)
        except Exception:
            return Response({"message": "Error al eliminar"}, 400)