from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import InscriptionForm
from .models import Categorie, Livre, Membre, Emprunt

# Create your views here.

def home(request):
    # Récupérer toutes les catégories
    categories = Categorie.objects.all()
    
    # Récupérer les 3 livres les plus récents
    recent_books = Livre.objects.order_by('-date_edition')[:3]
    
    context = {
        'categories': categories,
        'recent_books': recent_books,
    }
    
    return render(request, 'home.html', context)

def categorie(request, categorie_id):
    categories = Categorie.objects.all()  # Récupère toutes les catégories
    # Supposons que vous passiez l'ID de la catégorie en paramètre d'URL
    categorie = get_object_or_404(Categorie, id=categorie_id)  # Récupère la catégorie correspondant à l'ID
    livres = Livre.objects.filter(categorie=categorie)  # Filtrez les livres par catégorie

    context = {
        'categories': categories,
        'categorie': categorie,
        'livres': livres,
    }
    return render(request, 'categorie.html', context)

@login_required
def emprunt(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)  # Récupère le livre correspondant à l'ID
    livres_similaires = Livre.objects.filter(categorie=livre.categorie).exclude(id=livre.id)  # Autres livres de la même catégorie

    # Si l'utilisateur soumet un formulaire d'emprunt valide
    if request.method == "POST":
        # Traitement du formulaire d'emprunt
        duree = request.POST.get('duree')  # Récupère la durée depuis le formulaire
        paiement = request.POST.get('paiement')  # Récupère le mode de paiement

        # Vérifiez si l'utilisateur est authentifié
        if request.user.is_authenticated:
            # Enregistrer les informations de l'emprunt dans la base de données
            new_emprunt = Emprunt.objects.create(membre=request.user, livre=livre, duree=duree, paiement=paiement)

            # Rediriger vers la page de confirmation avec les deux ID
            return redirect('confirmation', livre_id=livre.id, emprunt_id=new_emprunt.id)
        else:
            # Rediriger vers la page de connexion si l'utilisateur n'est pas authentifié
            return redirect('connexion')  # Assurez-vous que l'URL 'login' existe

    context = {
        'livre': livre,  # Détails du livre emprunté
        'livres_similaires': livres_similaires,  # Autres livres similaires
        'categorie': livre.categorie,  # Catégorie du livre pour le lien "Voir plus"
    }
    return render(request, 'emprunt.html', context)


def connexion(request):
    if request.method == 'POST':
        noms = request.POST.get('noms')
        mot_de_passe = request.POST.get('mot_de_passe')
        user = authenticate(request, username=noms, password=mot_de_passe)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige vers la page d'accueil après la connexion réussie
        else:
            error_message = "Nom d'utilisateur ou mot de passe incorrect."
            return render(request, 'connexion.html', {'error_message': error_message})
    return render(request, 'connexion.html')

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            membre = form.save(commit=False)
            membre.set_password(form.cleaned_data['password1'])  # Hash le mot de passe
            membre.save()
            return redirect('connexion')  # Redirige vers la page de connexion après inscription
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form, 'errors': form.errors})

def logout_view(request):
    logout(request)
    return redirect('home')



@login_required
def confirmation(request, livre_id, emprunt_id):
    livre = get_object_or_404(Livre, id=livre_id)  # Récupère le livre correspondant à l'ID
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)

    # Vérifiez si l'utilisateur authentifié correspond au membre de l'emprunt
    if emprunt.membre == request.user:  # Utilisez `membre` au lieu de `user`
        context = {
            'livre': livre,
            'emprunt': emprunt,
            'categories': Categorie.objects.all(),  # Récupère toutes les catégories
        }
        return render(request, 'confirmation.html', context)
    else:
        # Rediriger vers la page de connexion ou une page d'erreur
        return redirect('connexion')