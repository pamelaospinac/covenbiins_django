from django.urls import path

from . import views

app_name = "covenbiins"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),

    path("listar_inmuebles/", views.inmuebles, name="listar_inmuebles"),
    path("form_inmuebles/", views.inmuebles_crear_formulario, name="form_inmuebles"),
    path("inmuebles_guardar/", views.inmuebles_guardar, name="inmuebles_guardar"),
    path("inmuebles_editar/<int:id_Inmueble>/", views.inmuebles_editar, name="inmuebles_editar"),
    path("inmuebles_buscar/", views.inmuebles_buscar, name="inmuebles_buscar"),
    path("inmuebles_eliminar/<int:id_Inmueble>/", views.inmuebles_eliminar, name="inmuebles_eliminar"),

    path("listar_usuarios/", views.usuarios, name="listar_usuarios"),
    path("usuarios_buscar/", views.usuarios_buscar, name="usuarios_buscar"),
    path("usuarios_eliminar/<int:cedula>/", views.usuarios_eliminar, name="usuarios_eliminar"),
    
    path("listar_citas/", views.citas, name="listar_citas"),
    path("form_citas/", views.citas_crear_formulario, name="form_citas"),
    path("citas_guardar/", views.citas_guardar, name="citas_guardar"),
    path("citas_editar/<int:id_Citas>/", views.citas_editar, name="citas_editar"),
    path("citas_buscar/", views.citas_buscar, name="citas_buscar"),
    path("citas_eliminar/<int:id_Citas>/", views.citas_eliminar, name="citas_eliminar"),

    path("listar_ratings/", views.ratings, name="listar_ratings"),
    path("form_rating/", views.rating_crear_formulario, name="form_rating"),
    path("ratings_buscar/", views.ratings_buscar, name="ratings_buscar"),
    path("ratings_eliminar/<int:id_Rating>/", views.ratings_eliminar, name="ratings_eliminar"),

    path("listar_aprobaciones/", views.aprobaciones, name="listar_aprobaciones"),
    path("aprobaciones_buscar/", views.aprobaciones_buscar, name="aprobaciones_buscar"),
    path("aprobaciones_eliminar/<int:id_Aprobacion>/", views.aprobaciones_eliminar, name="aprobaciones_eliminar"),

    path("listar_autenticaciones/", views.autenticaciones, name="listar_autenticaciones"),
    path("form_autent/", views.autenticaciones_crear_formulario, name="form_autent"),
    path("autenticaciones_guardar/", views.autenticaciones_guardar, name="autenticaciones_guardar"),
    path("form_edit_autent/<int:id_Autenticacion>", views.autenticaciones_editar_formulario, name="form_edit_autent"),
    path("autenticaciones_buscar/", views.autenticaciones_buscar, name="autenticaciones_buscar"),
    path("autenticaciones_eliminar/<int:id_Autenticacion>/", views.autenticaciones_eliminar, name="autenticaciones_eliminar"),
]

