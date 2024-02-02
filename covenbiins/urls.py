from django.urls import path

from . import views

app_name = "covenbiins"

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("register_guardar/", views.register_guardar, name="register_guardar"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),

    path("listar_inmuebles/", views.inmuebles, name="listar_inmuebles"),
    path("form_inmuebles/", views.inmuebles_crear_formulario, name="form_inmuebles"),
    path("inmuebles_guardar/", views.inmuebles_guardar, name="inmuebles_guardar"),
    path("inmuebles_editar/<int:id_Inmueble>/", views.inmuebles_editar, name="inmuebles_editar"),
    path("inmuebles_buscar/", views.inmuebles_buscar, name="inmuebles_buscar"),
    path("inmuebles_eliminar/<int:id_Inmueble>/", views.inmuebles_eliminar, name="inmuebles_eliminar"),

    path("listar_usuarios/", views.usuarios, name="listar_usuarios"),
    path("form_usuarios/", views.usuarios_crear_formulario, name="form_usuarios"),
    path("usuarios_guardar/", views.usuarios_guardar, name="usuarios_guardar"),
    path("usuarios_editar/<int:cedula>/", views.usuarios_editar, name="usuarios_editar"),
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
    path("rating_guardar/", views.rating_guardar, name="rating_guardar"),
    path("rating_editar/<int:id_Rating>/", views.rating_editar, name="rating_editar"),
    path("ratings_buscar/", views.ratings_buscar, name="ratings_buscar"),
    path("ratings_eliminar/<int:id_Rating>/", views.ratings_eliminar, name="ratings_eliminar"),

    path("listar_aprobaciones/", views.aprobaciones, name="listar_aprobaciones"),
    path("form_aprob/", views.aprobaciones_crear_formulario, name="form_aprob"),
    path("aprobaciones_guardar/", views.aprobaciones_guardar, name="aprobaciones_guardar"),
    path("aprobaciones_editar/<int:id_Aprobacion>/", views.aprobaciones_editar, name="aprobaciones_editar"),
    path("aprobaciones_buscar/", views.aprobaciones_buscar, name="aprobaciones_buscar"),
    path("aprobaciones_eliminar/<int:id_Aprobacion>/", views.aprobaciones_eliminar, name="aprobaciones_eliminar"),

]

