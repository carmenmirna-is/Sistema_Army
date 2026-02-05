from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilArmy, FotoGaleria, ListaPersonal


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Correo electrónico'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar contraseña'})


class PerfilArmyForm(forms.ModelForm):
    class Meta:
        model = PerfilArmy
        fields = [
            'nombre', 'genero', 'fecha_nacimiento', 'departamento', 'ciudad',
            'instagram', 'twitter', 'tiktok', 'spotify', 'bias_favorito',
            'ocupacion', 'sobre_mi', 'celular', 'foto_perfil'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu ciudad'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@tu_usuario'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@tu_usuario'}),
            'tiktok': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@tu_usuario'}),
            'spotify': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu usuario de Spotify'}),
            'bias_favorito': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RM, Jin, Suga, J-Hope, Jimin, V, Jungkook'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estudiante, Profesional, Emprendedor, etc.'}),
            'sobre_mi': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Cuéntanos algo sobre ti...'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+591 12345678'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
        }


class FotoGaleriaForm(forms.ModelForm):
    class Meta:
        model = FotoGaleria
        fields = ['foto', 'descripcion']
        widgets = {
            'foto': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción de la foto (opcional)'}),
        }


class ListaPersonalForm(forms.ModelForm):
    class Meta:
        model = ListaPersonal
        fields = ['titulo', 'contenido']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de tu lista'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Escribe tu lista aquí...'}),
        }