from django.db import models
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication

class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clave_admin = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    ocupacion = models.CharField(max_length=255, null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del admin " + self.user.first_name + " " + self.user.last_name


class Alumnos(models.Model):
    id = models.BigAutoField(primary_key=True)
    #si
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=255, null=True, blank=True)
    curp = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    ocupacion = models.CharField(max_length=255, null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del alumno " + self.user.first_name + " " + self.user.last_name


class Maestros(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_trabajador = models.CharField(max_length=255, null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    cubiculo = models.CharField(max_length=255, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    area_investigacion = models.CharField(max_length=255, null=True, blank=True)
    materias_json = models.TextField(null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del maestro " + self.user.first_name + " " + self.user.last_name



class Eventos(models.Model):
    TIPO_EVENTO_CHOICES = [
        ('Conferencia', 'Conferencia'),
        ('Taller', 'Taller'),
        ('Seminario', 'Seminario'),
        ('Concurso', 'Concurso'),
    ]

    PROGRAMA_CHOICES = [
        ('Ingeniería en Ciencias de la Computación', 'Ingeniería en Ciencias de la Computación'),
        ('Licenciatura en Ciencias de la Computación', 'Licenciatura en Ciencias de la Computación'),
        ('Ingeniería en Tecnologías de la Información', 'Ingeniería en Tecnologías de la Información'),
    ]

    id = models.BigAutoField(primary_key=True)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos_responsable')
    nombre = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=255, choices=TIPO_EVENTO_CHOICES, null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    lugar = models.CharField(max_length=255, null=True, blank=True)
    
    # OPCIONES PARA TIPO DE PÚBLICO
    es_estudiantes = models.BooleanField(default=False)
    es_profesores = models.BooleanField(default=False)
    es_publico = models.BooleanField(default=False)
    
    # TOMAR OPCION DE PROGRAMA EDUCATIVO
    programa = models.CharField(max_length=255, choices=PROGRAMA_CHOICES, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    cupo = models.IntegerField(null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Evento: " + (self.nombre)