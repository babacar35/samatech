# Generated by Django 5.0.3 on 2024-03-05 03:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conducteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('adresse', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=20)),
                ('numero_permis', models.CharField(max_length=20)),
                ('date_naissance', models.DateField()),
                ('date_embauche', models.DateField()),
                ('montant_journalier', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montant_semestriel', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montant_mensuel', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marque', models.CharField(max_length=100)),
                ('modele', models.CharField(max_length=100)),
                ('annee', models.IntegerField()),
                ('numero_immatriculation', models.CharField(max_length=20)),
                ('kilométrage', models.FloatField()),
                ('date_achat', models.DateField()),
                ('date_revision', models.DateField()),
                ('etat', models.CharField(max_length=50)),
                ('conducteur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_auto.conducteur')),
            ],
        ),
        migrations.CreateModel(
            name='AffectationVehiculeConducteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut_affectation', models.DateField()),
                ('date_fin_affectation', models.DateField()),
                ('conducteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_auto.conducteur')),
                ('vehicule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_auto.vehicule')),
            ],
        ),
        migrations.CreateModel(
            name='Versement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('type', models.CharField(choices=[('journalier', 'Journalier'), ('semestriel', 'Semestriel'), ('mensuel', 'Mensuel')], max_length=20)),
                ('conducteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_auto.conducteur')),
            ],
        ),
    ]
