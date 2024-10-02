from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import categorie, emprunt, connexion, inscription

urlpatterns = [
    path('', views.home, name='home'),
    path('categorie/<int:categorie_id>/', categorie, name='categorie'),
    path('emprunt/<int:livre_id>/', emprunt, name='emprunt'),
    path('confirmation/<int:livre_id>/<int:emprunt_id>/', views.confirmation, name='confirmation'),
    path('connexion/', connexion, name='connexion'),
    path('inscription/', inscription, name='inscription'),
    path('logout/', views.logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)