from django.contrib import admin
from django.utils.html import mark_safe

# Register your models here.
from .models import *


class InmueblesAdmin(admin.ModelAdmin):
    fields = ["nombre", "tipoInmueble", "descripcion", "precio", "direccion", "area", "habitaciones", "banos", "estrato", "categoria", "ciudad", "cedula", "imagen"]
    list_display = ["nombre", "tipoInmueble", "precio", "descripcion","area", "habitaciones", "banos", "estrato","cedula", "categoria", "ciudad", "imagen"]


class AprobacionesAdmin(admin.ModelAdmin):
    fields = ["nombreUsuario", "direccion", "copiaCedula", "certificadoLibertad", "cedula", "id_Inmueble"]
    list_display = ["nombreUsuario", "id_Inmueble", "cedula"]


class UsuariosAdmin(admin.ModelAdmin):
    fields = ["cedula", "nombre", "apellido", "fechaNacimiento", "telefono", "direccion", "tipoUsuario", "email", "contrasena", "foto"]
    list_display = ["cedula", "nombre", "apellido", "tipoUsuario", "email", "contrasena", "foto"]


class CitasAdmin(admin.ModelAdmin):
    fiels = ["horaCita", "usuario", "asesor", "estado"]
    list_display = ["horaCita", "usuario", "asesor", "estado"]


class ListaAdmin(admin.ModelAdmin):
    fields=["id_Inmueble", "cedula"]
    list_display = ["id_Lista", "id_Inmueble", "cedula"]


class InformeAdmin(admin.ModelAdmin):
    fields=["nombreInforme", "inmueble", "fechaInforme", "descripcion"]
    list_display = ["nombreInforme", "inmueble", "fechaInforme", "descripcion", "citas", "cedula"]


class ChatAdmin(admin.ModelAdmin):
    list_display =['fecha', 'mensaje', 'usuario_origen', 'usuario_destino']

admin.site.register(Inmuebles, InmueblesAdmin)
admin.site.register(Aprobaciones, AprobacionesAdmin)
admin.site.register(Usuarios, UsuariosAdmin)
admin.site.register(Citas, CitasAdmin)
admin.site.register(Lista,ListaAdmin)
admin.site.register(Informe,InformeAdmin)
admin.site.register(Chat,ChatAdmin)