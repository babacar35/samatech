from django.db import models
from django.urls import reverse

# Create your models here.

from django.utils.text import slugify
from django.contrib.auth.models import User
class Vehicule(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    annee = models.IntegerField()
    numero_immatriculation = models.CharField(max_length=20)
    kilométrage = models.FloatField()
    date_achat = models.DateField()
    date_revision = models.DateField()
    etat = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos/vehicules/', null=True, blank=True)
    conducteur = models.ForeignKey('Conducteur', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.marque)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.numero_immatriculation})"

class Conducteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    numero_permis = models.CharField(max_length=20)
    date_naissance = models.DateField()
    date_embauche = models.DateField()
    montant_journalier = models.DecimalField(max_digits=10, decimal_places=2)
    montant_semestriel = models.DecimalField(max_digits=10, decimal_places=2)
    montant_mensuel = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='photos/conducteurs/', null=True, blank=True)

    #def get_absolute_url(self):
        #return reverse('admin:gestion_auto_conducteur_change', args=[str(self.pk)])

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class AffectationVehiculeConducteur(models.Model):
    vehicule = models.ForeignKey('Vehicule', on_delete=models.CASCADE)
    conducteur = models.ForeignKey('Conducteur', on_delete=models.CASCADE)
    #contrat = models.ImageField(upload_to='photos/Contrats/', null=True, blank=True)
    date_debut_affectation = models.DateField()
    date_fin_affectation = models.DateField()
    
    def __str__(self):
        return f"{self.conducteur} - {self.vehicule}"

class Versement(models.Model):
    conducteur = models.ForeignKey('Conducteur', on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    TYPE_CHOICES = [
        ('journalier', 'Journalier'),
        ('semestriel', 'Semestriel'),
        ('mensuel', 'Mensuel'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.conducteur} - {self.montant} - {self.date}"
    
class Frais(models.Model):
    date = models.DateField()
    TYPE_CHOICES = [
        ('depenses_supplementaire', 'Depenses Supplementaire'),
        ('depannage', 'Depannage'),
     
    ]
    type = models.CharField(max_length=25, choices=TYPE_CHOICES)

    description = models.CharField(max_length=255)
    cout = models.DecimalField(max_digits=10, decimal_places=2)
    Facture = models.ImageField(upload_to='photos/Factures/', null=True, blank=True)
    vehicule = models.ForeignKey('Vehicule', on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Frais"

# class Test(models.Model):
#     date = models.DateField()
#     contrats = models.ImageField(upload_to='photos/Contrats/', null=True, blank=True)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez les champs nécessaires pour synchroniser avec le modèle du tableau de bord Material
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
