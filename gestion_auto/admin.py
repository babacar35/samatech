from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm
# Register your models here.
from .models import Vehicule, Conducteur, AffectationVehiculeConducteur, Versement , Frais

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ['marque', 'modele', 'annee', 'numero_immatriculation', 'kilométrage', 'etat', 'conducteur']

@admin.register(Conducteur)
class ConducteurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'adresse', 'telephone', 'numero_permis', 'date_naissance', 'date_embauche', 'montant_journalier', 'montant_semestriel', 'montant_mensuel']
    search_fields = ('nom','prenom','numero_permis')  # Champ pour la recherche par nom de conducteur
    #list_filter = ('date_naissance',)  # Filtre par date

@admin.register(AffectationVehiculeConducteur)
class AffectationVehiculeConducteurAdmin(admin.ModelAdmin):
    list_display = ['vehicule', 'conducteur', 'date_debut_affectation', 'date_fin_affectation',]

@admin.register(Versement)
class VersementAdmin(admin.ModelAdmin):
    list_display = ['conducteur', 'montant', 'date', 'type']
    search_fields = ('conducteur__nom','type')  # Champ pour la recherche par nom de conducteur
    list_filter = ('date',)  # Filtre par date

@admin.register(Frais)
class FraisAdmin(admin.ModelAdmin):
    list_display = ['date', 'type', 'description', 'cout','vehicule','Facture']
    search_fields = ('type',)  # Champ pour la recherche par nom de conducteur
    list_filter = ('date',)  # Filtre par date





class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    form = UserProfileForm

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
