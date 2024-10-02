from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

# Gestionnaire de membres personnalisés
class MembreManager(BaseUserManager):
    def create_user(self, noms, password=None, **extra_fields):
        if not noms:
            raise ValueError('Le nom doit être fourni')
        
        # Créer l'utilisateur
        membre = self.model(noms=noms, **extra_fields)
        
        # Définir le mot de passe
        if password:
            membre.set_password(password)  # Hacher le mot de passe
        else:
            membre.set_password(self.make_random_password())  # Générer un mot de passe par défaut

        membre.save(using=self._db)
        return membre

    def create_superuser(self, noms, password=None, **extra_fields):
        # Configuration des champs spécifiques pour le superutilisateur
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(noms, password, **extra_fields)

# Modèle Membre
class Membre(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    noms = models.CharField(max_length=100, unique=True, verbose_name="Nom complet")
    date_adhesion = models.DateField(auto_now_add=True, verbose_name="Date d'adhésion")
    image = models.ImageField(upload_to='auth/images/', blank=True, null=True, verbose_name="Image de profil")
    
    # Champs de gestion
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_staff = models.BooleanField(default=False, verbose_name="Membre du staff")
    
    # Configuration du gestionnaire
    objects = MembreManager()

    # Définition de USERNAME_FIELD et REQUIRED_FIELDS
    USERNAME_FIELD = 'noms'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.noms
    
# Modèle Auteur
class Auteur(models.Model):
    id = models.AutoField(primary_key=True)
    noms = models.CharField(max_length=100)

    def __str__(self):
        return self.noms 

# Modèle Categorie
class Categorie(models.Model):
    id = models.AutoField(primary_key=True)
    noms = models.CharField(max_length=100)
    qte_livre = models.IntegerField()  # Retiré max_digit

    def __str__(self):
        return self.noms 

# Modèle Livre
class Livre(models.Model):
    id = models.AutoField(primary_key=True)
    noms = models.CharField(max_length=100)
    date_edition = models.DateField()
    auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE)  # Renommé
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)  # Renommé
    image = models.ImageField(upload_to='livre/images/', blank=True, null=True)

    def __str__(self):
        return self.noms 

# Modèle Emprunt
class Emprunt(models.Model):
    PAIEMENT_CHOICES = [
        ('MM', 'Mobile Money'),
        ('CC', 'Credit Card'),
        ('BTC', 'Bitcoin'),
    ]

    id = models.AutoField(primary_key=True)
    duree = models.IntegerField()  # Stocke la durée en jours
    paiement = models.CharField(max_length=10, choices=PAIEMENT_CHOICES, default='MM')  # Champ avec des choix
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)  # Clé étrangère vers Membre
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)  # Clé étrangère vers Livre

    def __str__(self):
        return f"Emprunt de {self.livre.noms} par {self.membre.noms} pour {self.duree} jours"