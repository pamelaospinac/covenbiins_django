from django.urls import path

from . import views

app_name = "covenbiins"

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("register_guardar/", views.register_guardar, name="register_guardar"),

    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),

    path("cambiar_clave/<str:actual>", views.cambiar_clave, name="cambiar_clave"),
    path("guardar_clave/", views.guardar_clave, name="guardar_clave"),
    path("perfil/", views.ver_perfil, name="perfil"),

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

    path("listar_aprobaciones/", views.aprobaciones, name="listar_aprobaciones"),
    path("form_aprob/", views.aprobaciones_crear_formulario, name="form_aprob"),
    path("aprobaciones_guardar/", views.aprobaciones_guardar, name="aprobaciones_guardar"),
    path("aprobaciones_editar/<int:id_Aprobacion>/", views.aprobaciones_editar, name="aprobaciones_editar"),
    path("aprobaciones_buscar/", views.aprobaciones_buscar, name="aprobaciones_buscar"),
    path("aprobaciones_eliminar/<int:id_Aprobacion>/", views.aprobaciones_eliminar, name="aprobaciones_eliminar"),

    path("publicar/", views.publicar_inmueble, name="publicar"),
    path("guardar_publicacion/", views.publicacion_guardar, name="guardar_publicaion"),

    path("asesoria_legal/", views.asesoria_legal, name="asesoria_legal"),
    path("asignar_cita/", views.asignar_cita, name="asignar_cita"),
    path("informe_guardar/", views.generar_informe, name="informe_guardar"),
    path("informe/<int:id_Citas>/", views.form_informe, name="informe"),

    path("catalogo/", views.catalogo, name="catalogo"),
    path("catalogo_buscar/", views.buscar_catalogo, name="catalogo_buscar"),
    path("detalle/<int:id_Inmueble>/", views.detalle, name="detalle"),
    path("lista_deseos/", views.lista_deseos, name="lista_deseos"),
    path("lista_agregar/", views.lista_agregar, name="lista_agregar"),

    path("chat/", views.chat, name="chat"),
    path("ver_chat/<int:cedula>/", views.ver_chat, name="ver_chat"),
    path("add_chat/", views.add_chat, name="add_chat"),
    
]

