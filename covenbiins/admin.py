from django.contrib import admin
from django.utils.html import mark_safe

# Register your models here.
from .models import *


class InmueblesAdmin(admin.ModelAdmin):
    fields = ["nombre", "tipoInmueble", "descripcion", "precio", "direccion", "cedula"]
    list_display = ["nombre", "tipoInmueble", "precio", "descripcion", "cedula"]


class AprobacionesAdmin(admin.ModelAdmin):
    fields = ["nombreUsuario", "direccion", "copiaCedula", "certificadoLibertad", "cedula", "id_Inmueble"]
    list_display = ["nombreUsuario", "id_Inmueble", "cedula"]


class UsuariosAdmin(admin.ModelAdmin):
    fields = ["cedula", "nombre", "apellido", "fechaNacimiento", "telefono", "direccion", "tipoUsuario",
              "email", "contrasena", "foto"]
    list_display = ["cedula", "nombre", "apellido", "tipoUsuario", "email", "contrasena"]


class RatingsAdmin(admin.ModelAdmin):
    fields = ["calificacion", "cedula"]
    list_display = ["cedula", "calificacion"]


class CitasAdmin(admin.ModelAdmin):
    fiels = ["horaCita", "usuario", "asesor"]
    list_display = ["horaCita", "usuario", "asesor"]


admin.site.register(Inmuebles, InmueblesAdmin)
admin.site.register(Aprobaciones, AprobacionesAdmin)
admin.site.register(Usuarios, UsuariosAdmin)
admin.site.register(Ratings, RatingsAdmin)
admin.site.register(Citas, CitasAdmin)
