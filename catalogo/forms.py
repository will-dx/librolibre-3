from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Mensaje, ContactoMensaje
from .models import Libro


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'id': 'password', 'placeholder': 'Mínimo 8 caracteres', 'minlength': 8,
        }),
    )

    class Meta:
        model = CustomUser
        fields = ['nombre', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'id': 'nombre', 'placeholder': 'Tu nombre completo', 'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'id': 'email', 'placeholder': 'ejemplo@universidad.edu', 'autocomplete': 'email',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = 'Nombre completo'
        self.fields['email'].label = 'Correo institucional'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label='Correo institucional',
        widget=forms.EmailInput(attrs={
            'id': 'email', 'placeholder': 'ejemplo@universidad.edu',
            'autocomplete': 'email', 'autofocus': True,
        }),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'id': 'password', 'placeholder': '••••••••', 'autocomplete': 'current-password',
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError('Correo o contraseña incorrectos.')
            self.user_cache = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'estado', 'foto', 'materia']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'id': 'titulo', 'placeholder': 'Ej: Cálculo Diferencial', 'autofocus': True,
            }),
            'autor': forms.TextInput(attrs={
                'id': 'autor', 'placeholder': 'Ej: Juan Pérez López',
            }),
            'estado': forms.Select(attrs={'id': 'estado'}),
            'foto': forms.FileInput(attrs={'id': 'foto', 'accept': 'image/*'}),
            'materia': forms.Select(attrs={'id': 'materia'}),
        }
        labels = {
            'titulo': 'Título del libro',
            'autor': 'Autor',
            'estado': 'Estado del libro',
            'foto': 'Foto del libro',
            'materia': 'Materia',
        }


class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['destinatario', 'contenido']
        widgets = {
            'destinatario': forms.Select(attrs={'id': 'destinatario'}),
            'contenido': forms.Textarea(attrs={
                'id': 'contenido', 'placeholder': 'Escribe tu mensaje...', 'rows': 5,
            }),
        }
        labels = {
            'destinatario': 'Para',
            'contenido': 'Mensaje',
        }

    def __init__(self, *args, **kwargs):
        remitente = kwargs.pop('remitente', None)
        super().__init__(*args, **kwargs)
        if remitente:
            self.fields['destinatario'].queryset = CustomUser.objects.exclude(id=remitente.id)
        else:
            self.fields['destinatario'].queryset = CustomUser.objects.all()
        self.fields['destinatario'].empty_label = 'Selecciona un destinatario'


class RespuestaMensajeForm(forms.Form):
    contenido = forms.CharField(
        label='Respuesta',
        widget=forms.Textarea(attrs={
            'id': 'contenido', 'placeholder': 'Escribe tu respuesta...', 'rows': 4,
        }),
    )


class PerfilForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nombre', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'id': 'nombre', 'placeholder': 'Tu nombre completo', 'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'id': 'email', 'placeholder': 'ejemplo@universidad.edu', 'autocomplete': 'email',
            }),
        }
        labels = {
            'nombre': 'Nombre completo',
            'email': 'Correo institucional',
        }


class CambioPasswordForm(forms.Form):
    password_actual = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={
            'id': 'password_actual', 'placeholder': 'Tu contraseña actual',
        }),
    )
    nueva_password = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'id': 'nueva_password', 'placeholder': 'Mínimo 8 caracteres', 'minlength': 8,
        }),
    )
    confirmar_password = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'id': 'confirmar_password', 'placeholder': 'Repite la nueva contraseña',
        }),
    )

    def clean_nueva_password(self):
        password = self.cleaned_data.get('nueva_password')
        validate_password(password)
        return password


class ContactoForm(forms.ModelForm):
    class Meta:
        model = ContactoMensaje
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'id': 'nombre', 'placeholder': 'Tu nombre completo', 'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'id': 'email', 'placeholder': 'tu@correo.com', 'autocomplete': 'email',
            }),
            'asunto': forms.TextInput(attrs={
                'id': 'asunto', 'placeholder': '¿Sobre qué trata tu mensaje?',
            }),
            'mensaje': forms.Textarea(attrs={
                'id': 'mensaje', 'placeholder': 'Escribe tu mensaje...', 'rows': 6,
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'email': 'Correo',
            'asunto': 'Asunto',
            'mensaje': 'Mensaje',
        }


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        # Definimos solo los campos que el usuario va a llenar en la web
        # Excluimos 'usuario' para que Django no lo pida como obligatorio en el HTML
        fields = ['titulo', 'autor', 'estado', 'foto', 'materia']

        # Opcional: Esto añade los mismos placeholders de tu HTML original
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Ej: Cálculo Diferencial',
                'autofocus': 'autofocus'
            }),
            'autor': forms.TextInput(attrs={
                'placeholder': 'Ej: Juan Pérez López'
            }),
        }