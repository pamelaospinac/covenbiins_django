from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.db.models import Q

from django.contrib import messages

from .models import *


# Create your views here.


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        contrasena = request.POST.get("contrasena")
        try:
            q = Autenticaciones.objects.get(email=email, contrasena=contrasena)
            messages.success(request, "Bienvenido!!")
            datos = {
                "id_Autenticacion": q.id_Atenticacion,
                "email": q.email,
                "contrasena": q.contrasena,
            }
            request.session["logueo"] = datos
            return HttpResponseRedirect(reverse("covenbiins:index"))
        except Autenticaciones.DoesNotExist:
            messages.error(request, "Usuarios o contraseñas no validos")
            return render(request, "covenbiins:index")
    else:
        if request.session.get("logueo", False):
            return HttpResponseRedirect(reverse("covenbiins:index"))
        else:
            return render(request, "covenbiins:index")


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
        usu = Usuarios.objects.get(pk=request.POST.get("usuario"))

        if id_Inmueble == "":
            try:
                inm = Inmuebles(
                    nombre=nomb,
                    precio=prec,
                    descripcion=desc,
                    direccion=direc,
                    tipoInmueble=tipo,
                    usuarios=usu,
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
        return HttpResponseRedirect(reverse("covenbiins/citas/form_citas.html", contexto))


def citas_editar(request, id_Citas):
    q = Citas.objects.get(pk=id_Citas)
    query = Usuarios.objects.all()
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
    pass


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


def autenticaciones(request):
    result = Autenticaciones.objects.all()
    context = {"data": result}
    return render(request, "covenbiins/autenticaciones/listar_autenticaciones.html", context)


def autenticaciones_crear_formulario(request):
    return render(request, "covenbiins/autenticaciones/form_autent.html")


def autenticaciones_guardar(request):
    if request.method == "POST":
        id_Autenticacion = request.POST.get("id")
        em = request.POST.get("correo")
        con = request.POST.get("contrasena")

        if id_Autenticacion == "":
            try:
                aut = Autenticaciones(
                    email=em,
                    contrasena=con,
                )
                aut.save()
                messages.success(request, "Guardado correctamente")
            except Exception as e:
                messages.error(request, f"Error. {e}")
        else:
            try:
                q = Autenticaciones.objects.get(pk=id_Autenticacion)
                q.email = em
                q.save()
                messages.success(request, "Actualizado correctamente")
            except Exception as e:
                messages.error(request, f"Error2. {e}")

        return HttpResponseRedirect(reverse("covenbiins:listar_autenticaciones", args=()))
    else:
        messages.warning(request, "NO se enviaron datos")
        return render(request, "covenbiins:form_autent", args=())


def autenticaciones_editar_formulario(request, id_Autenticacion):
    q = Autenticaciones.objects.get(pk=id_Autenticacion)
    contexto = {"id": id_Autenticacion, "data": q}
    return render(request, "covenbiins/autenticaciones/form_autent.html", contexto)


def autenticaciones_buscar(request):
    if request.method == "POST":

        buscar = request.POST.get("buscar")

        query = Autenticaciones.objects.filter(email__icontains=buscar)

        context = {"data": query, "buscado": buscar}
        return render(request, "covenbiins/autenticaciones/listar_autenticaciones.html", context)
    else:
        messages.warning(request, "No se enviaron datos")
    return HttpResponseRedirect(reverse("covenbiins:autenticaciones", args=()))


def autenticaciones_eliminar(request, id_Autenticacion):
    try:
        q = Autenticaciones.objects.get(pk=id_Autenticacion)
        q.delete()
        messages.success(request, "Registro eliminado correctamente")
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return HttpResponseRedirect(reverse("covenbiins:listar_autenticaciones", args=()))
