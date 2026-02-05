from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class PerfilArmy(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('N', 'Prefiero no decir'),
    ]
    
    DEPARTAMENTO_CHOICES = [
        ('SCZ', 'Santa Cruz'),
        ('LPZ', 'La Paz'),
        ('CBBA', 'Cochabamba'),
        ('CHQ', 'Chuquisaca'),
        ('TJA', 'Tarija'),
        ('ORU', 'Oruro'),
        ('PTS', 'Potosí'),
        ('BEN', 'Beni'),
        ('PND', 'Pando'),
    ]
    
    # Usuario asociado (uno a uno)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_army')
    
    # Datos personales
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    departamento = models.CharField(max_length=4, choices=DEPARTAMENTO_CHOICES, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    
    # Redes sociales
    instagram = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    tiktok = models.CharField(max_length=100, blank=True)
    spotify = models.CharField(max_length=100, blank=True)
    
    # BTS Info
    bias_favorito = models.CharField(max_length=100, blank=True, help_text="Tu miembro favorito de BTS")
    
    # Ocupación
    ocupacion = models.CharField(max_length=200, blank=True)
    
    # Sobre mí
    sobre_mi = models.TextField(blank=True, help_text="Cuéntanos algo sobre ti")
    
    # Contacto
    phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$', message="El número debe estar en formato: '+591 12345678'")
    celular = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Foto de perfil
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'army_perfilarmy'  # ← AGREGAR ESTO
        verbose_name = "Perfil ARMY"
        verbose_name_plural = "Perfiles ARMY"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} (@{self.usuario.username})"
    
    def edad(self):
        if self.fecha_nacimiento:
            from datetime import date
            today = date.today()
            edad = today.year - self.fecha_nacimiento.year
            if today.month < self.fecha_nacimiento.month or (today.month == self.fecha_nacimiento.month and today.day < self.fecha_nacimiento.day):
                edad -= 1
            return edad
        return None


class FotoGaleria(models.Model):
    perfil = models.ForeignKey(PerfilArmy, on_delete=models.CASCADE, related_name='galeria')
    foto = models.ImageField(upload_to='galeria/')
    descripcion = models.CharField(max_length=200, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'army_fotogaleria'  # ← AGREGAR ESTO
        verbose_name = "Foto de Galería"
        verbose_name_plural = "Fotos de Galería"
        ordering = ['-fecha_subida']
    
    def __str__(self):
        return f"Foto de {self.perfil.nombre} - {self.fecha_subida.strftime('%d/%m/%Y')}"


class ListaPersonal(models.Model):
    perfil = models.ForeignKey(PerfilArmy, on_delete=models.CASCADE, related_name='listas')
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'army_listapersonal'  # ← AGREGAR ESTO
        verbose_name = "Lista Personal"
        verbose_name_plural = "Listas Personales"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.perfil.nombre}"