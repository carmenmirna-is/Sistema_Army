from django.contrib import admin
from .models import PerfilArmy, FotoGaleria, ListaPersonal


@admin.register(PerfilArmy)
class PerfilArmyAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'genero', 'departamento', 'bias_favorito', 'fecha_creacion')
    list_filter = ('genero', 'departamento', 'fecha_creacion')
    search_fields = ('nombre', 'usuario__username', 'ciudad', 'bias_favorito')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    
    fieldsets = (
        ('Usuario', {
            'fields': ('usuario',)
        }),
        ('Información Personal', {
            'fields': ('nombre', 'genero', 'fecha_nacimiento', 'departamento', 'ciudad', 'celular')
        }),
        ('Redes Sociales', {
            'fields': ('instagram', 'twitter', 'tiktok', 'spotify')
        }),
        ('BTS Info', {
            'fields': ('bias_favorito',)
        }),
        ('Ocupación y Descripción', {
            'fields': ('ocupacion', 'sobre_mi')
        }),
        ('Foto', {
            'fields': ('foto_perfil',)
        }),
        ('Metadata', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FotoGaleria)
class FotoGaleriaAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'descripcion', 'fecha_subida')
    list_filter = ('fecha_subida',)
    search_fields = ('perfil__nombre', 'descripcion')
    readonly_fields = ('fecha_subida',)


@admin.register(ListaPersonal)
class ListaPersonalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'perfil', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('titulo', 'perfil__nombre', 'contenido')
    readonly_fields = ('fecha_creacion',)