from django.db import models

# Create your models here.


class Inmuebles(models.Model):
    id_Inmueble = models.BigAutoField(unique=True, primary_key=True)
    nombre = models.CharField(max_length=50)
    tipoInmueble = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    precio = models.IntegerField()
    direccion = models.CharField(max_length=50)
    imagen = models.CharField(max_length=50, null=True)
    cedula = models.ForeignKey('Usuarios', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.id_Inmueble}"


class Aprobaciones(models.Model):
    id_Aprobacion = models.BigAutoField(unique=True, primary_key=True)
    nombreUsuario = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    copiaCedula = models.CharField(max_length=50)
    certificadoLibertad = models.CharField(max_length=50)
    id_Inmueble = models.ForeignKey('Inmuebles', on_delete=models.DO_NOTHING)
    cedula = models.ForeignKey('Usuarios', on_delete=models.DO_NOTHING)


class Usuarios(models.Model):
    Roles = (
        (1, 'Administrador'),
        (2, 'Asesor Legal'),
        (3, 'Vendedor'),
        (4, "Comprador"),
    )
    cedula = models.CharField(unique=True, primary_key=True, max_length=10)
    foto = models.ImageField(null=True, blank=True, default='fotos/default.png', upload_to='fotos')
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fechaNacimiento = models.DateField()
    telefono = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    tipoUsuario = models.IntegerField(choices=Roles, default=4)
    email = models.EmailField(unique=True, null=True)
    contrasena = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.cedula}"


class Ratings(models.Model):
    id_Rating = models.BigAutoField(unique=True, primary_key=True)
    calificacion = models.IntegerField()
    cedula = models.ForeignKey('Usuarios', on_delete=models.DO_NOTHING)


class Citas(models.Model):
    id_Citas = models.BigAutoField(primary_key=True, blank=True)
    horaCita = models.DateTimeField()
    usuario = models.ForeignKey('Usuarios', on_delete=models.CASCADE, related_name='UsuarioFk')
    asesor = models.ForeignKey('Usuarios', on_delete=models.CASCADE, related_name='AsesorFk')

