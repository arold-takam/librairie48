from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Membre

# Formulaire d'inscription
class InscriptionForm(forms.ModelForm):
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, min_length=6)
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput, min_length=6)

    class Meta:
        model = Membre
        fields = ['noms', 'image']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data

# Formulaire de connexion
class ConnexionForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

# Formulaire de mise à jour du profil
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['noms', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['noms'].required = True
        self.fields['image'].required = False
