from django.shortcuts import render ,get_object_or_404


# Create your views here.
from django.http import HttpResponse
#les modeles
from .models import Vehicule, Conducteur, Versement, AffectationVehiculeConducteur,Frais

# Dans votre vue Django

# import matplotlib.pyplot as plt
# import pandas as pd

#paginations 
from django.core.paginator import Paginator

from django.db.models import Sum 

# views.py

from django.contrib.auth.models import User

# views.py

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('admin:index')  # Redirection pour les superutilisateurs vers l'interface d'administration
        else:
            return reverse_lazy('gestion_auto_accueil')  # Redirection pour les utilisateurs normaux vers une autre vue


def gestion_auto_accueil(request):
    # Calculer le nombre de véhicules
    nombre_vehicules = Vehicule.objects.count()
    from decimal import Decimal

    total_frais = Frais.objects.aggregate(total=Sum('cout'))
    depenses_total = Decimal(total_frais['total']) 
    total_versement = Versement.objects.aggregate(total=Sum('montant'))
    revenues_total = round(Decimal(total_versement['total']),3) 
    
    # Calculer le nombre de conducteurs
    nombre_conducteurs = Conducteur.objects.count()
    context = {
        'nombre_vehicules': nombre_vehicules,
        'nombre_conducteurs': nombre_conducteurs,
        'depenses':depenses_total,
        'revenues':revenues_total}

    return render(request,'gestion_auto/gestion_auto_index.html',context)

def login(request):
    return render(request, 'gestion_auto/login.html')


def profile(request):
    user = request.User  # Récupérer l'utilisateur connecté
    return render(request, 'pages/profile.html', {'user': user})



def conducteurs_tables(request):
    conducteurs = Conducteur.objects.all()
    return render(request, 'pages/tables.html', {'conducteurs': conducteurs})

def info_affectation_versement(request, affectation_id):
    # Logique de votre vue ici 
    return render(request, 'gestion_auto/info_affectation_versement.html', {'affectation_id': affectation_id})


def accueil2(request):
    vehicules = Vehicule.objects.filter(id=1).values()
    marque=vehicules[0]['marque']
    photo = vehicules[0]['photo']
    context = {
        'marque': marque,
        'photo':photo
        
    }
    return render(request, 'gestion_auto/accueil.html',context)

#------------------------------------------------------------- ---------------------------- -----------------------
#recuperation jointure table vehicule et conducteur
affectations = AffectationVehiculeConducteur.objects.select_related('conducteur', 'vehicule')
conducteurs = []
for affectation in affectations:
        versement = Versement.objects.filter(conducteur=affectation.conducteur).first()
        conducteurs.append({'affectation': affectation, 'type_versement': versement.type if versement else None})
#------------------------------------ ----------------------------- ------------------------ ----------------------
        
def tab(request):

    #paginator = Paginator(conducteurs, 5)  # 10 conducteurs par page

    #page_number = request.GET.get('page')
    #page_obj = paginator.get_page(page_number)
    
    return render(request, 'gestion_auto/accueil.html',{'conducteurs': conducteurs})

def conducteurs_vehicules(request):
   
    return render(request, 'gestion_auto/conducteurs_vehicules.html', {'conducteurs': conducteurs})
    
#------------------------------------------------------------- ---------------------------- -----------------------


def detail_vehicule(request,slug):
    #vehicule = get_object_or_404(Vehicule, pk=vehicule_id)
    vehicule = get_object_or_404(Vehicule, slug=slug)
    return render(request, 'gestion_auto/detail_vehicule.html', {'vehicule': vehicule})





def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    vehicules = Vehicule.objects.all()
    return render(request, 'gestion_auto/index.html',{'vehicules': vehicules})

#test de vue dashboard

def dashboard(request):
    vehicules = Vehicule.objects.all()
    conducteurs = Conducteur.objects.all()
    context = {
        'vehicules': vehicules,
        'conducteurs': conducteurs,
    }
    return render(request, 'gestion_auto/dashboard.html',context)

#testons le nouveau template



def accueil(request):
    # Calculer le nombre de véhicules
    nombre_vehicules = Vehicule.objects.count()
    #depenses totals
    # frais = Frais.objects.all()

    # # Initialiser le total à 0
    # depenses_total = 0

    # # Parcourir tous les enregistrements de frais et additionner les coûts
    # for frais_item in frais:
    #     depenses_total += frais_item.cout
    from decimal import Decimal

    total_frais = Frais.objects.aggregate(total=Sum('cout'))
    depenses_total = Decimal(total_frais['total']) 
    total_versement = Versement.objects.aggregate(total=Sum('montant'))
    revenues_total = Decimal(total_versement['total']) 
    

    print(type(depenses_total))
    # Calculer le nombre de conducteurs
    nombre_conducteurs = Conducteur.objects.count()

    # Calculer le montant total versé par conducteur
    montant_total_par_conducteur = {}
    conducteurs = Conducteur.objects.all()
    for conducteur in conducteurs:
        montant_total_par_conducteur[conducteur.nom] = Versement.objects.filter(conducteur=conducteur).aggregate(Sum('montant'))['montant__sum'] or 0

    context = {
        'nombre_vehicules': nombre_vehicules,
        'nombre_conducteurs': nombre_conducteurs,
        'montant_total_par_conducteur': montant_total_par_conducteur,
        'depenses':depenses_total,
        'revenues':revenues_total
    }
    return render(request, 'gestion_auto/test.html', context)




def test(request):
    # Calcul du nombre de véhicules, de conducteurs et des montants totaux versés par conducteur
    nb_vehicules = Vehicule.objects.count()
    nb_conducteurs = Conducteur.objects.count()
    montants_par_conducteur = Versement.objects.values('conducteur').annotate(total_montant=Sum('montant')).order_by('-total_montant')
    #depenses totals
    # Récupérer tous les enregistrements de frais
    frais = Frais.objects.all()

    # Initialiser le total à 0
    depenses_total = 0

    # Parcourir tous les enregistrements de frais et additionner les coûts
    for frais_item in frais:
        depenses_total += frais_item.cout


    #depenses_total = Frais.objects.all().aggregate(Sum('cout')).values()
    # Préparation des données pour le graphique d'évolution des versements
    versements_journaliers = Versement.objects.filter(type='journalier').values('date').annotate(total_versement=Sum('montant'))
    versements_semestriels = Versement.objects.filter(type='semestriel').values('date').annotate(total_versement=Sum('montant'))
    versements_mensuels = Versement.objects.filter(type='mensuel').values('date').annotate(total_versement=Sum('montant'))

    context = {
        'nb_vehicules': nb_vehicules,
        'nb_conducteurs': nb_conducteurs,
        'montants_par_conducteur': montants_par_conducteur,
        'versements_journaliers': versements_journaliers,
        'versements_semestriels': versements_semestriels,
        'versements_mensuels': versements_mensuels,
        'depenses':depenses_total
    }

    return render(request, 'gestion_auto/test2.html', context)


