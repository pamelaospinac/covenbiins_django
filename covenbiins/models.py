from django.db import models


# Create your models here.


class Inmuebles(models.Model):
    Categoria = (
        (1, 'Usado'),
        (2, 'Nuevo')
    )
    id_Inmueble = models.BigAutoField(unique=True, primary_key=True)
    nombre = models.CharField(max_length=50)
    tipoInmueble = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    precio = models.IntegerField()
    direccion = models.CharField(max_length=50)
    categoria = models.IntegerField(choices=Categoria, default=1)
    ciudad = models.CharField(max_length=50, null=True)
    area = models.IntegerField()
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    estrato = models.IntegerField(null= True)
    imagen = models.ImageField(default="fotos_inmuebles/default.png", upload_to='fotos_inmuebles')
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
        (4, 'Comprador'),
    )
    cedula = models.CharField(unique=True, primary_key=True, max_length=10)
    foto = models.ImageField(null=True, blank=True, default='fotos/default.jpeg', upload_to='fotos')
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


class Citas(models.Model):
    ESTADO = (
        (1, 'Asignada'),
        (2, 'Realizada'),
        (3, 'Cancelada')
    )
    id_Citas = models.BigAutoField(primary_key=True, blank=True)
    horaCita = models.DateTimeField()
    usuario = models.ForeignKey('Usuarios', on_delete=models.CASCADE, related_name='UsuarioFk')
    asesor = models.ForeignKey('Usuarios', on_delete=models.CASCADE, related_name='AsesorFk')
    estado = models.IntegerField(choices=ESTADO, default=1)

class Lista(models.Model):
    id_Lista  = models.BigAutoField(primary_key=True, blank=True)
    id_Inmueble = models.ForeignKey('Inmuebles', on_delete=models.DO_NOTHING)
    cedula = models.ForeignKey('Usuarios', on_delete=models.DO_NOTHING)

class Informe(models.Model):
    id_Informe = models.BigAutoField(primary_key=True, blank=True) 
    nombreInforme = models.CharField(max_length=50)
    inmueble = models.CharField(max_length=50)
    fechaInforme = models.DateField()
    descripcion = models.CharField(max_length=3500)
    citas = models.ForeignKey('Citas', on_delete=models.DO_NOTHING)
    cedula = models.ForeignKey('Usuarios', on_delete=models.DO_NOTHING, null=True)

class Chat(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    mensaje = models.CharField(max_length=254)
    usuario_origen = models.ForeignKey(Usuarios, related_name="usuarios_fk1", on_delete=models.DO_NOTHING)
    usuario_destino = models.ForeignKey(Usuarios, related_name="usuarios_fk2", on_delete=models.DO_NOTHING)
