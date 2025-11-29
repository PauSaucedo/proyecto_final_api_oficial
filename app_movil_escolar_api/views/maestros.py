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
        lista = MaestroSerializer(maestros, many=True).data

        lista_final = []

        for maestro in lista:
            if "user" in maestro and isinstance(maestro["user"], dict):
                maestro["first_name"] = maestro["user"].get("first_name", "")
                maestro["last_name"] = maestro["user"].get("last_name", "")
                maestro["email"] = maestro["user"].get("email", "")
            if isinstance(maestro.get("materias_json"), str):
                try:
                    maestro["materias_json"] = json.loads(maestro["materias_json"])
                except:
                    maestro["materias_json"] = []

            lista_final.append(maestro)

        return Response(lista_final, 200)

class MaestrosView(generics.CreateAPIView):

    # --- ESTE GET PREPARA LOS DATOS PARA QUE EL FORMULARIO NO SALGA VACÍO ---
    def get(self, request, *args, **kwargs):
        maestro_id = request.query_params.get('id')
        if maestro_id:
            maestro = get_object_or_404(Maestros, id=maestro_id)
            serializer = MaestroSerializer(maestro)
            
            # 1. Convertimos a dict para poder modificar (IMPORTANTE)
            data = dict(serializer.data)

            # 2. APLANAR DATOS (Sacar nombre, apellido, email del objeto 'user')
            if 'user' in data and data['user']:
                user_data = data.pop('user')
                data['first_name'] = user_data.get('first_name', '')
                data['last_name'] = user_data.get('last_name', '')
                data['email'] = user_data.get('email', '')
                data['rol'] = 'maestro'

            # 3. CORREGIR MATERIAS (Convertir de Texto a Lista real)
            if "materias_json" in data and data["materias_json"]:
                try:
                    if isinstance(data["materias_json"], str):
                        data["materias_json"] = json.loads(data["materias_json"])
                except Exception:
                    data["materias_json"] = []
            
            return Response(data, 200)
        
        return Response({"error": "ID no proporcionado"}, 400)
    # ---------------------------------------------------------------

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
            
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                return Response({"message": "Username "+email+", is already taken"}, 400)

            user = User.objects.create(username=email, email=email, first_name=first_name, last_name=last_name, is_active=1)
            user.set_password(password)
            user.save()
            
            group, created = Group.objects.get_or_create(name=role)
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
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        maestro = get_object_or_404(Maestros, id=request.data["id"])
        maestro.id_trabajador = request.data["id_trabajador"]
        maestro.telefono = request.data["telefono"]
        maestro.rfc = request.data["rfc"]
        maestro.cubiculo = request.data["cubiculo"]
        maestro.area_investigacion = request.data["area_investigacion"]
        # Convertimos la lista a string para guardarla en BD
        maestro.materias_json = json.dumps(request.data["materias_json"])
        maestro.save()
        
        user = maestro.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()
        
        return Response({"message": "Maestro actualizado correctamente", "maestro": MaestroSerializer(maestro).data}, 200)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        maestro = get_object_or_404(Maestros, id=request.GET.get("id"))
        try:
            maestro.user.delete()
            return Response({"details": "Maestro eliminado"}, 200)
        except Exception:
            return Response({"details": "Algo pasó al eliminar"}, 400)