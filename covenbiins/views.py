from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import datetime

from django.db.models import Q

from django.contrib import messages
from django.core.mail import BadHeaderError, EmailMessage

from covenbiins_django import settings
from .models import *


# Create your views here.


def register(request):  # Aqui se redirecciona al form del registro
    result = Usuarios.objects.all()
    context = {"usuarios": result}
    return render(request, "covenbiins/register.html", context)


def register_guardar(request):  # Aqui se hace el proceso de registro
    if request.method == "POST":
        cedula = request.POST.get("cedula")
        nom = request.POST.get("nombre")
        ape = request.POST.get("apellido")
        fecha = request.POST.get("fechaNacimiento")
        tel = request.POST.get("telefono")
        direc = request.POST.get("direccion")
        email = request.POST.get("email")
        password = request.POST.get("contrasena")

        try:
            usu = Usuarios(
                cedula=cedula,
                nombre=nom,
                apellido=ape,
                fechaNacimiento=fecha,
                telefono=tel,
                direccion=direc,
                email=email,
                contrasena=password
            )
            usu.save()
            messages.success(request, "Registrado")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return HttpResponseRedirect(reverse("covenbiins:index", args=()))
    else:
        messages.warning(request, "No se enviaron datos")
        return HttpResponseRedirect(reverse("covenbiins:register"))


def login(request):  # Aqui se hace el proceso de login
    if request.method == "POST":
        email = request.POST.get("email")
        contrasena = request.POST.get("contrasena")
        try:
            u = Usuarios.objects.get(email=email, contrasena=contrasena)
            messages.success(request, "Bienvenido!!")
            datos = {
                "nombre": u.nombre,
                "email": u.email,
                "contrasena": u.contrasena,
                "rol": u.tipoUsuario,
                "nombre_tipoUsaurio": u.get_tipoUsuario_display(),
                "cedula": u.cedula,
                "foto": u.foto.url if u.foto else "media/fotos/default.jpeg",
            }
            request.session["logueo"] = datos
            return HttpResponse(request, "Okay")
        except Usuarios.DoesNotExist:
            messages.error(request, "Usuario o contraseña no validos")
            return HttpResponse(request, "Malo")
    else:
        pass


def logout(request):  # Aqui se hace el proceso de cerrar sesion
    try:
        del request.session["logueo"]
        messages.success(request, "Sesion Cerrada")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return HttpResponseRedirect(reverse("covenbiins:index"))


def index(request):  # Aqui se redirecciona a la vista principal y se manda la informacion necesaria
    if request.session.get("logueo", False):
        usuario = request.session.get("logueo", False)
        q = Usuarios.objects.get(pk=usuario["cedula"])
        result = Citas.objects.filter(asesor=q)
        a = Usuarios.objects.all()
        context = {"citas": result, "asesor": a}
        print(f"{result}")
        return render(request, "covenbiins/index.html", context)
    else:
        return render(request, "covenbiins/index.html")


def cambiar_clave(request, actual):  # Aqui se redirecciona al form de cambio de clave
    context = {"actual": actual}

    return render(request, "covenbiins/usuarios/cambio_clave.html", context)


def guardar_clave(request):  # Aqui se hace el proceso de cambio de clave
    usuario = request.session.get("logueo", False)
    if usuario:
        if request.method == "POST":
            actual = request.POST.get("actual")
            clave1 = request.POST.get("clave1")
            clave2 = request.POST.get("clave2")
            try:
                q = Usuarios.objects.get(pk=usuario["cedula"], contrasena=actual)
                if clave1 == clave2:
                    q.contrasena = clave1
                    q.save()
                    messages.success(request, "Contraseña actualizada correctamente")
                else:
                    messages.warning(request, "Las contraseñas no coinciden")

            except Exception as e:
                messages.warning(request, "Contraseña no válida")
                return HttpResponseRedirect(reverse("covenbiins:cambiar_clave", kwargs={'actual': actual}))
        return HttpResponseRedirect(reverse("covenbiins:index"))
    else:
        return HttpResponseRedirect(reverse("covenbiins:index"))


def ver_perfil(request):  # Aqui redirecciona al el perfil del usuario y manda la informacion necesaria
    usuario = request.session.get("logueo", False)
    q = Usuarios.objects.get(pk=usuario["cedula"])
    contexto = {"data": q}
    return render(request, "covenbiins/usuarios/perfil.html", contexto)


# Creacion del crud de cada Tabla de la BD
def inmuebles(request):
    result = Inmuebles.objects.all()
    context = {"data": result}
    return render(request, "covenbiins/inmuebles/listar_inm.html", context)


def inmuebles_crear_formulario(request):
    result = Usuarios.objects.all()
    context = {"usuarios": result}
    return render(request, "covenbiins/inmuebles/form_inmuebles.html", context)


def inmuebles_guardar(request):
    if request.method == "POST":
        id_Inmueble = request.POST.get("id")
        nomb = request.POST.get("nombre")
        prec = request.POST.get("precio")
        desc = request.POST.get("descripcion")
        direc = request.POST.get("direccion")
        tipo = request.POST.get("tipoInmueble")
        cedula = Usuarios.objects.get(pk=request.POST.get("cedula"))

        if id_Inmueble == "":
            try:
                inm = Inmuebles(
                    nombre=nomb,
                    precio=prec,
                    descripcion=desc,
                    direccion=direc,
                    tipoInmueble=tipo,
                    cedula=cedula,
                )
                inm.save()
                messages.success(request, "Guardado correctamente")
            except Exception as e:
                messages.error(request, f"Error2:{e}")
        else:
            try:
                q = Inmuebles.objects.get(pk=id_Inmueble)
                q.nombre = nomb
                q.precio = prec
                q.descripcion = desc
                q.direccion = direc
                q.tipoInmueble = tipo
                q.cedula = cedula
                q.save()
                messages.success(request, "Actualizado correctamente")
            except Exception as e:
                messages.error(request, f"Error: {e}")

        return HttpResponseRedirect(reverse("covenbiins:listar_inmuebles", args=()))
    else:
        messages.warning(request, "No se enviaron datos")
        return HttpResponseRedirect(reverse("covenbiins:form_inmuebles", args=()))


def inmuebles_editar(request, id_Inmueble):
    q = Inmuebles.objects.get(pk=id_Inmueble)
    query = Usuarios.objects.all()
    contexto = {"id": id_Inmueble, "data": q, "usuarios": query}
    return render(request, "covenbiins/inmuebles/form_inmuebles.html", contexto)


def inmuebles_buscar(request):
    if request.method == "POST":
        buscar = request.POST.get("buscar")

        query = Inmuebles.objects.filter(id_Inmueble__icontains=buscar)

        context = {"data": query, "buscado": buscar}
        return render(request, "covenbiins/inmuebles/listar_inm.html", context)
    else:
        messages.warning(request, "NO se enviaron datos")
    return HttpResponseRedirect(reverse("covenbiins:inmuebles", args=()))


def inmuebles_eliminar(request, id_Inmueble):
    try:
        q = Inmuebles.objects.get(pk=id_Inmueble)
        q.delete()
        messages.success(request, "Registro eliminado correctamente")
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return HttpResponseRedirect(reverse("covenbiins:listar_inmuebles", args=()))


def usuarios(request):
    result = Usuarios.objects.all()
    context = {"data": result}
    return render(request, "covenbiins/usuarios/listar_usu.html", context)


def usuarios_crear_formulario(request):
    query = Usuarios.objects.all()
    context = {"data": query}
    return render(request, "covenbiins/usuarios/form_usuario.html", context)


def usuarios_guardar(request):
    if request.method == "POST":
        cedula = request.POST.get("cedula")
        nom = request.POST.get("nombre")
        rol = request.POST.get("tipoUsuario")

        if cedula == "":
            try:
                usu = Usuarios(
                    cedula=cedula,
                    nombre=nom,
                    tipoUsuario=rol,
                )
                usu.save()
                messages.success(request, "Guardado correctamente")
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            try:
                q = Usuarios.objects.get(pk=cedula)
                q.cedula = cedula
                q.nombre = nom
                q.tipoUsuario = rol
                q.save()
                messages.success(request, "Actualizado correctamente")
            except Exception as e:
                messages.error(request, f"Error2: {e}")

        return HttpResponseRedirect(reverse("covenbiins:listar_usuarios", args=()))
    else:
        messages.warning(request, "No se enviaron datos")
        return HttpResponseRedirect(reverse("covenbiins:form_usuarios", args=()))


def usuarios_editar(request, cedula):
    q = Usuarios.objects.get(pk=cedula)
    contexto = {"id": cedula, "data": q}
    return render(request, "covenbiins/usuarios/form_usuario.html", contexto)


def usuarios_buscar(request):
    if request.method == "POST":

        buscar = request.POST.get("buscar")

        query = Usuarios.objects.filter(cedula__icontains=buscar)

        context = {"data": query, "buscado": buscar}
        return render(request, "covenbiins/usuarios/listar_usu.html", context)
    else:
        messages.warning(request, "No se enviaron datos")
    return HttpResponseRedirect(reverse("covenbiins:usuarios", args=()))


def usuarios_eliminar(request, cedula):
    try:
        q = Usuarios.objects.get(pk=cedula)
        q.delete()
        messages.success(request, "Registro eliminado correctamente")
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return HttpResponseRedirect(reverse("covenbiins:listar_usuarios", args=()))


def citas(request):
    result = Citas.objects.all()
    context = {"data": result}
    return render(request, "covenbiins/citas/listar_citas.html", context)


def citas_crear_formulario(request):
    query = Usuarios.objects.all()
    context = {"usuarios": query}
    return render(request, "covenbiins/citas/form_citas.html", context)


def citas_guardar(request):
    if request.method == "POST":
        id_Citas = request.POST.get("id")
        hora = request.POST.get("horaCita")
        usu = Usuarios.objects.get(pk=request.POST.get("usuario"))
        ase = Usuarios.objects.get(pk=request.POST.get("asesor"))

        if id_Citas == "":
            try:
                cita = Citas(
                    horaCita=hora,
                    usuario=usu,
                    asesor=ase,
                )
                cita.save()
                messages.success(request, "Guardado correctamente")
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            try:
                q = Citas.objects.get(pk=id_Citas)
                q.horaCita = hora
                q.usuario = usu
                q.asesor = ase
                q.save()
                messages.success(request, "Actualizado correctamente")
            except Exception as e:
                messages.error(request, f"Error: {e}")

        return HttpResponseRedirect(reverse("covenbiins:listar_citas", args=()))
    else:
        messages.warning(request, "No se enviaron datos")
        return HttpResponseRedirect(reverse("covenbiins:form_citas", args=()))


def citas_editar(request, id_Citas):
    q = Citas.objects.get(pk=id_Citas)
    query = Usuarios.objects.all()
    q.horaCita = q.horaCita.strftime('%Y-%m-%dT%H:%M')
    contexto = {"id": id_Citas, "data": q, "usuarios": query}
    return render(request, "covenbiins/citas/form_citas.html", contexto)


def citas_buscar(request):
    if request.method == "POST":

        buscar = request.POST.get("buscar")

        query = Citas.objects.filter(id_Citas__icontains=buscar)

        context = {"data": query, "buscado": buscar}
        return render(request, "covenbiins/citas/listar_citas.html", context)
    else:
        messages.warning(request, "NO se enviaron datos")
    return HttpResponseRedirect(reverse("covenbiins:citas", args=()))


def citas_eliminar(request, id_Citas):
    try:
        q = Citas.objects.get(pk=id_Citas)
        q.delete()
        messages.success(request, "Registro eliminado correctamente")
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return HttpResponseRedirect(reverse("covenbiins:listar_citas", args=()))


def aprobaciones(request):
    result = Aprobaciones.objects.all()
    context = {"data": result}
    return render(request, "covenbiins/aprobaciones/listar_aprob.html", context)


def aprobaciones_crear_formulario(request):
    query = Usuarios.objects.all()
    Q = Aprobaciones.objects.all()
    resultado = Inmuebles.objects.all()
    context = {"usuarios": query, "aprobaciones": Q, "inmuebles": resultado}
    return render(request, "covenbiins/aprobaciones/form_aprob.html", context)


def aprobaciones_guardar(request):
    if request.method == "POST":
        id_Aprobacion = request.POST.get("id")
        nomb = request.POST.get("nombre")
        inm = Inmuebles.objects.get(pk=request.POST.get("inmueble"))
        cedula = Usuarios.objects.get(pk=request.POST.get("cedula"))

        if id_Aprobacion == "":
            try:
                apro = Aprobaciones(
                    nombre=nomb,
                    inmueble=inm,
                    cedula=cedula,
                )
                apro.save()
                messages.success(request, "Guardado correctamente")
            except Exception as e:
                messages.error(request, f"Error. {e}")
        else:
            try:
                q = Aprobaciones.objects.get(pk=id)
                q.nombre = nomb
                q.inmueble = inm
                q.cedula = cedula
                q.save()
                messages.success(request, "Actualizado correctamente")
            except Exception as e:
                messages.error(request, f"2Error. {e}")

        return HttpResponseRedirect(reverse("covenbiins:listar_aprobaciones", args=()))
    else:
        messages.warning(request, "No se enviaron datos")
        return HttpResponseRedirect(reverse("covenbiins:form_aprob", args=()))


def aprobaciones_editar(request, id_Aprobacion):
    q = Aprobaciones.objects.get(pk=id_Aprobacion)
    result = Aprobaciones.objects.all()
    resultado = Inmuebles.objects.all()
    query = Usuarios.objects.all()
    contexto = {"id": id_Aprobacion, "data": q, "usuarios": query, "aprobaciones": result, "inmuebles": resultado}
    return render(request, "covenbiins/aprobaciones/form_aprob.html", contexto)


def aprobaciones_buscar(request):
    if request.method == "POST":

        buscar = request.POST.get("buscar")

        query = Aprobaciones.objects.filter(id_Aprobacion__icontains=buscar)

        context = {"data": query, "buscado": buscar}
        return render(request, "covenbiins/aprobaciones/listar_aprob.html", context)
    else:
        messages.warning(request, "No se enviaron datos")
    return HttpResponseRedirect(reverse("covenbiins:aprobaciones", args=()))


def aprobaciones_eliminar(request, id_Aprobacion):
    try:
        q = Aprobaciones.objects.get(pk=id_Aprobacion)
        q.delete()
        messages.success(request, "Registro eliminado correctamente")
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return HttpResponseRedirect(reverse("covenbiins:listar_aprobaciones", args=()))


# Aqui termina

def publicar_inmueble(request):  # Aqui redirecciona al form de publicar inmueble
    result = Inmuebles.objects.all()
    context = {"inmuebles": result}
    return render(request, "covenbiins/publicar/publicar.html", context)


def upload_file(f, nuevo_nombre):
    with open(f"uploads/fotos_inmuebles/{nuevo_nombre}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def publicacion_guardar(request):  # Aqui hace el proceso de creacion y guardado
    usuario = request.session.get("logueo", False)
    if request.method == "POST":
        q = Usuarios.objects.get(pk=usuario["cedula"])
        nomb = request.POST.get("nombre")
        desc = request.POST.get("descripcion")
        cat = request.POST.get("tipoInmueble")
        prec = request.POST.get("precio")
        direc = request.POST.get("direccion")
        est = request.POST.get("categoria")
        ciu = request.POST.get("ciudad")
        area = request.POST.get("area")
        habit = request.POST.get("habitaciones")
        banos = request.POST.get("banos")
        estrato = request.POST.get("estrato")
        img = request.FILES.get("imagen")
        if img is not None:
            ahora = datetime.datetime.now()
            print(ahora)
            ahora = str(ahora).replace("-", "").replace(":", "").replace(".", "_")
            print(ahora)
            nombre_foto = img.name.rsplit('.', 1)
            nuevo_nombre = f"{nombre_foto[0]}_{ahora}.{nombre_foto[1]}"
            upload_file(img, nuevo_nombre)
        else:
            nuevo_nombre = "default.png"
        try:
            inm = Inmuebles(
                nombre=nomb,
                tipoInmueble=cat,
                descripcion=desc,
                precio=prec,
                direccion=direc,
                categoria=est,
                ciudad=ciu,
                area=area,
                habitaciones=habit,
                banos=banos,
                estrato=estrato,
                imagen=f"fotos_inmuebles/{nuevo_nombre}",
                cedula=q
            )
            inm.save()
            messages.success(request, f"Publicado")
            return HttpResponseRedirect(reverse("covenbiins:index"))
        except Exception as e:
            messages.error(request, f"Error {e}")
            return HttpResponseRedirect(reverse("covenbiins:publicar"))
    else:
        messages.warning(request, "No se enviaron datos")
        return HttpResponseRedirect(reverse("covenbiins:publicar"))


def asesoria_legal(request):  # Aqui redirecciona a ver tus citas, el form para asignar y manda la informacion necesaria
    usuario = request.session.get("logueo", False)
    q = Usuarios.objects.get(pk=usuario["cedula"])
    result = Citas.objects.filter(usuario=q)
    a = Usuarios.objects.all()
    context = {"citas": result, "asesor": a}
    return render(request, "covenbiins/asesoria_legal/index.html", context)


def asignar_cita(request):  # Aqui crea y guarda la cita
    usuario = request.session.get("logueo", False)
    if request.method == "POST":
        q = Usuarios.objects.get(pk=usuario["cedula"])
        hora = request.POST.get("HoraCita")
        aser = Usuarios.objects.get(pk=request.POST.get("asesor"))

        try:
            cita = Citas(
                horaCita=hora,
                usuario=q,
                asesor=aser,
            )
            cita.save()
            messages.success(request, "La cita fue asignada correctamente")
            try:
                destinatario = "emmaupegui2005@gmail.com"
                mensaje = f"""
                            <h1> Cita Asignada </h1>
                            <strong> Asesor: {cita.asesor.nombre} </strong>
                            <h3>Hora cita: {cita.horaCita}</h3>
                            <p>Recuerda que si quires cancelar la cita, debes hacerlo <strong>maximo 3 horas</strong> antes de la misma.</p><br>
                            <strong>Si deseas cancelar la cita dar click al siguiente botón:</strong><br><br>
                            <button class="btn btn-danger">Cancelar Cita</button>
                        """
                try:
                    msg = EmailMessage("Confirmacion Cita", mensaje, settings.EMAIL_HOST_USER, [destinatario])
                    msg.content_subtype = "html"
                    msg.send()
                except BadHeaderError:
                    print("Invalied header found.")
                except Exception as e:
                    print(f"error{e}")
            except Exception as e:
                messages.error(request, f"Error {e}")
        except Exception as e:
            messages.error(request, f"Error {e}")
    else:
        messages.warning(request, "No se enviaron datos")
    return HttpResponseRedirect(reverse("covenbiins:asesoria_legal"))


def catalogo(request):  # Aqui redirecciona a la vista de catalalogo y manda la informacionde la BD necesaria
    if request.session.get("logueo", False):
        i = Inmuebles.objects.all()
        context = {"inmuebles": i}
        return render(request, "covenbiins/catalogo/catalogo.html", context)


def buscar_catalogo(request):
    if request.method == "POST":

        cat = request.POST.get("categoria")
        tip = request.POST.get("tipoInmueble")
        cid = request.POST.get("ciudad")

        c = Inmuebles.objects.filter(id_Inmueble__icontains={cat, tip, cid})

        context = {"cat": c, "buscado": {cat, tip, cid}}
        return render(request, "covenbiins/catalogo/catalogo.html", context)
    else:
        messages.warning(request, "No se enviaron datos")
    return HttpResponseRedirect(reverse("covenbiins:catalogo", args=()))


def detalle(request, id_Inmueble):  # Aqui redirecciona a la vista de detalle y manda la informacion necesaria
    q = Inmuebles.objects.get(pk=id_Inmueble)
    # q.cedula = int(q.Usuarios.cedula)
    print(type(q.cedula.cedula))
    user = request.session.get("logueo", False)
    print(type(user["cedula"]))
    if q.cedula.cedula == user["cedula"]:
        print("Holap")
    query = Usuarios.objects.all()
    context = {"id": id_Inmueble, "data": q, "usuarios": query}
    return render(request, "covenbiins/catalogo/detalle.html", context)


def lista_agregar(request):  # Guarda el inmueble en una lista de deseos
    if request.session.get("logueo", False):
        usuario = request.session.get("logueo", False)
        if request.method == "POST":
            q = Usuarios.objects.get(pk=usuario["cedula"])
            inm = request.POST.get("id")
            try:
                inm_id = Inmuebles.objects.get(pk=inm)
                list = Lista(
                    id_Inmueble=inm_id,
                    cedula=q
                )
                list.save()
                messages.success(request, f"Guardado")
            except Exception as e:
                messages.error(request, f"Error {e}")
        return render(request, "covenbiins/catalogo/detalle.html")


def lista_deseos(request):  # Muestra los inmuebles que el usuario guarde en la lista de deseos
    if request.session.get("logueo", False):
        usuario = request.session.get("logueo", False)
        q = Usuarios.objects.get(pk=usuario["cedula"])
        inm = Lista.objects.filter(cedula=q)
        context = {"data": inm}
        return render(request, "covenbiins/lista_deseos/lista.html", context)


def form_informe(request, id_Citas):  # Redirecciona al from informe
    c = Citas.objects.get(pk=id_Citas)
    context = {"c": c}
    return render(request, "covenbiins/asesoria_legal/informe.html", context)


def generar_informe(request):  # Crea y guarda la informacion del informe
    if request.session.get("logueo", False):
        usuario = request.session.get("logueo", False)
        if request.method == "POST":
            q = Usuarios.objects.get(pk=usuario["cedula"])
            inm = request.POST.get("id")
            i = Citas.objects.get(pk=inm)
            nomb = request.POST.get("nombre")
            cat = request.POST.get("categoria")
            fecha = request.POST.get("fecha")
            desc = request.POST.get("descripcion")
            try:
                inf = Informe(
                    nombreInforme=nomb,
                    inmueble=cat,
                    fechaInforme=fecha,
                    descripcion=desc,
                    citas=i,
                    cedula=q
                )
                inf.save()
                messages.success(request, "Informe Generado")
                return HttpResponseRedirect(reverse("covenbiins:index"))
            except Exception as e:
                messages.error(request, f"Error: {e}")
                return render(request, "covenbiins/asesoria_legal/informe.html")


def chat(request):
    usuario = request.session.get("logueo", False)
    yo = Usuarios.objects.get(pk=usuario["cedula"])

    q = Usuarios.objects.filter((~Q(pk=yo)))
    context = {"usuarios": q}
    return render(request, "covenbiins/chat/usuarios_chat.html", context)


def ver_chat(request, cedula):
    usuario = request.session.get("logueo", False)

    yo = Usuarios.objects.get(pk=usuario["cedula"])
    otro = Usuarios.objects.get(pk=cedula)

    q = Chat.objects.filter(
        Q(usuario_origen=yo, usuario_destino=otro) | Q(usuario_origen=otro, usuario_destino=yo)).order_by('fecha')

    context = {"chat": q, "otro": otro}
    return render(request, "covenbiins/chat/ver_chat.html", context)


def add_chat(request):
    usuario = request.session.get("logueo", False)

    yo = Usuarios.objects.get(pk=usuario["cedula"])
    otro = Usuarios.objects.get(pk=request.POST.get("destino"))
    mensaje = request.POST.get("mensaje")
    try:
        q = Chat(
            mensaje=mensaje,
            usuario_origen=yo,
            usuario_destino=otro
        )
        q.save()
        messages.success(request, "Mensaje enviado!!")
    except Exception as e:
        messages.warning(request, "No se pudo enviar el mensaje, intente de nuevo....")

    return HttpResponseRedirect(reverse("covenbiins:ver_chat", args=(otro,)))


def deseo_eliminar(request, id_Lista):
    try:
        q = Lista.objects.get(pk=id_Lista)
        q.delete()
        messages.success(request, "Inmueble eliminado de tu lista de deseos")
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return HttpResponseRedirect(reverse("covenbiins:lista_deseos", args=()))


def recuperar_cuenta(request):
    if request.method == "POST":
        correo = request.POST.get('email')
        try:
            q = Usuarios.objects.get(email=correo)
            if q == correo:
                recuperar = True
            else:
                recuperar= False
        except Exception as e:
            return render(request, "covenbiins/index.html")


    return render(request, "covenbiins/recuperar_cuenta.html")
