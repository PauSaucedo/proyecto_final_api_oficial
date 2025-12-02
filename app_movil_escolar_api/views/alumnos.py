from django.db.models import *
from django.db import transaction
from app_movil_escolar_api.serializers import UserSerializer, AlumnoSerializer
from app_movil_escolar_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

class AlumnosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        alumnos = Alumnos.objects.filter(user__is_active=1).order_by("id")
        lista = AlumnoSerializer(alumnos, many=True).data
        return Response(lista, 200)

class AlumnosView(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        alumno = get_object_or_404(Alumnos, id=request.query_params.get('id'))
        serializer = AlumnoSerializer(alumno)
        return Response(serializer.data, 200)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
            
            if User.objects.filter(email=email).exists():
                return Response({"message": "Username "+email+", is already taken"}, 400)

            user = User.objects.create(username=email, email=email, first_name=first_name, last_name=last_name, is_active=1)
            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            alumno = Alumnos.objects.create(
                user=user,
                matricula=request.data["matricula"],
                curp=request.data["curp"].upper(),
                rfc=request.data["rfc"].upper(),
                fecha_nacimiento=request.data["fecha_nacimiento"],
                edad=request.data["edad"],
                telefono=request.data["telefono"],
                ocupacion=request.data["ocupacion"]
            )
            alumno.save()
            return Response({"alumno_created_id": alumno.id}, 201)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

class AlumnosViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        alumno = get_object_or_404(Alumnos, id=request.data["id"])
        alumno.matricula = request.data["matricula"]
        alumno.telefono = request.data["telefono"]
        alumno.rfc = request.data["rfc"]
        alumno.edad = request.data["edad"]
        alumno.ocupacion = request.data["ocupacion"]
        alumno.save()
        
        user = alumno.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()
        
        return Response({"message": "Alumno actualizado correctamente"}, 200)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        alumno = get_object_or_404(Alumnos, id=request.GET.get("id"))
        try:
            alumno.user.delete() # Borra usuario y cascada al alumno
            return Response({"message": "Alumno eliminado correctamente"}, 200)
        except Exception as e:
            return Response({"message": "No se pudo eliminar"}, 400)