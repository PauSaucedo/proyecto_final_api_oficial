from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# ... tus otros imports ...
from app_movil_escolar_api.views import bootstrap
from app_movil_escolar_api.views import users
from app_movil_escolar_api.views import alumnos
from app_movil_escolar_api.views import maestros
from app_movil_escolar_api.views import auth
from app_movil_escolar_api.views import eventos


urlpatterns = [
    # === CORRECCIÓN IMPORTANTE ===
    # 1. Recuperamos el Admin Oficial de Django (el panel azul)
    path('admin/', admin.site.urls),  # <--- ¡Esta línea es la clave del éxito! 🔑

    # 2. Movemos TU vista personalizada a otra ruta para no estorbar
    # Le cambié el nombre a 'crear-admin/' para que no choque.
    path('crear-admin/', users.AdminView.as_view()), 

    #Admin Data
    path('lista-admins/', users.AdminAll.as_view()),
    #Edit Admin
    path('admins-edit/', users.AdminsViewEdit.as_view()),

    # ... El resto de tus rutas déjalas igual ...
    
    #Create Alumno
    path('alumnos/', alumnos.AlumnosView.as_view()),
    path('lista-alumnos/', alumnos.AlumnosAll.as_view()),
    path('alumnos-edit/', alumnos.AlumnosViewEdit.as_view()),

    #Create Maestro
    path('maestros/', maestros.MaestrosView.as_view()),
    path('lista-maestros/', maestros.MaestrosAll.as_view()),
    path('maestros-edit/', maestros.MaestrosViewEdit.as_view()),
        
    #Create Evento
    path('eventos/', eventos.EventosView.as_view()),
    path('lista-eventos/', eventos.EventosAll.as_view()), 
    path('eventos-edit/', eventos.EventosViewEdit.as_view()),

    #Total Users
    path('total-usuarios/', users.TotalUsers.as_view()),
        
    #Login
    path('login/', auth.CustomAuthToken.as_view()),
    #Logout
    path('logout/', auth.Logout.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)