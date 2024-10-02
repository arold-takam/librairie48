from django.contrib import admin
from .models import Membre, Auteur, Categorie, Livre, Emprunt

# Register your models here.

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ('id', 'noms', 'image', 'date_adhesion', 'is_active', 'is_staff')
    search_fields = ('noms',)
    list_filter = ('is_active', 'is_staff', 'date_adhesion')

# Personnalisation de l'affichage du modèle Auteur
@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('id', 'noms')
    search_fields = ('noms',)

# Personnalisation de l'affichage du modèle Categorie
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('id', 'noms', 'qte_livre')
    search_fields = ('noms',)

# Personnalisation de l'affichage du modèle Livre
@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('id', 'noms', 'image', 'date_edition', 'auteur', 'categorie')
    search_fields = ('noms', 'auteur__noms', 'categorie__noms')
    list_filter = ('date_edition', 'categorie')

# Personnalisation de l'affichage du modèle Emprunt
@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ('id', 'livre', 'membre', 'duree', 'paiement')
    search_fields = ('livre__noms', 'membre__noms')
    list_filter = ('paiement', 'duree')

