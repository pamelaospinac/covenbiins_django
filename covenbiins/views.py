from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.db.models import Q

from django.contrib import messages

from .models import *


# Create your views here.


def register(request):
    result = Usuarios.objects.all()
    context = {"usuarios": result}
    return render(request, "covenbiins/register.html", context)


def register_guardar(request):
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

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        contrasena = request.POST.get("contrasena")
        try:
            u = Usuarios.objects.get(email=email, contrasena=contrasena)
            messages.success(request, "Bienvenido!!")
            datos = {
                "email": u.email,
                "contrasena": u.contrasena,
                "rol": u.tipoUsuario
            }
            request.session["logueo"] = datos
            return HttpResponse(request, "Okay")
        except Autenticaciones.DoesNotExist:
            messages.error(request, "Usuario o contraseña no validos")
            return HttpResponse(request, "Malo")
    else:
        pass


def logout(request):
    try:
        del request.session["logueo"]
        messages.success(request, "Sesion Cerrada")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return HttpResponseRedirect(reverse("covenbiins:index"))


def index(request):
    return render(request, "covenbiins/index.html")


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


def ratings(request):
    result = Ratings.objects.all()
    context = {"data": result}
    return render(request, "covenbiins/ratings/listar_rating.html", context)


def rating_crear_formulario(request):
    query = Usuarios.objects.all()
    context = {"usuarios": query}
    return render(request, "covenbiins/ratings/form_rating.html", context)


def rating_guardar(request):
    if request.method == "POST":
        id_Rating = request.POST.get("id")
        cal = request.POST.get("calificacion")
        cedula = Usuarios.objects.get(pk=request.POST.get("cedula"))

        if id_Rating == "":
            try:
                rat = Ratings(
                    calificacion=cal,
                    cedula=cedula,
                )
                rat.save()
                messages.success(request, "Guardado correctamente")
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            try:
                q = Ratings.objects.get(pk=id_Rating)
                q.calificacion = cal
                q.cedula = cedula
                q.save()
                messages.success(request, "Actualizado correctamente")
            except Exception as e:
                messages.error(request, f"2Error: {e}")

        return HttpResponseRedirect(reverse("covenbiins:listar_ratings", args=()))
    else:
        messages.warning(request, "No se enviaron datos")
        return HttpResponseRedirect(reverse("covenbiins:form_rating", args=()))


def rating_editar(request, id_Rating):
    q = Ratings.objects.get(pk=id_Rating)
    query = Usuarios.objects.all()
    contexto = {"id": id_Rating, "data": q, "usuarios": query}
    return render(request, "covenbiins/ratings/form_rating.html", contexto)


def ratings_buscar(request):
    if request.method == "POST":

        buscar = request.POST.get("buscar")

        query = Ratings.objects.filter(id_Rating__icontains=buscar)

        context = {"data": query, "buscado": buscar}
        return render(request, "covenbiins/ratings/listar_rating.html", context)
    else:
        messages.warning(request, "No se enviaron datos")
    return HttpResponseRedirect(reverse("covenbiins:ratings", args=()))


def ratings_eliminar(request):
    try:
        q = Ratings.objects.get(pk=id_Rating)
        q.delete()
        messages.success(request, "Registro eliminado correctamente")
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return HttpResponseRedirect(reverse("covenbiins:listar_rating", args=()))


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


0


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
