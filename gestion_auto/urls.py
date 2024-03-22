
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from .views import CustomLoginView
from . import views

urlpatterns = [
    path("infos_vehicule", views.index, name="index"),
    #path('accounts/login/', CustomLoginView.as_view(), name='login'),  # U
    path("", views.gestion_auto_accueil, name="gestion_auto_accueil"),
    #path('profile/', views.profile, name='profile'),
    path("tables", views.conducteurs_tables, name="conducteurs_tables"),
    # path("test", views.accueil, name="accueil"),
    # path("accueil", views.tab, name="accueil2"),
    # path("test2", views.test, name="test"),
    # path("test3", views.conducteurs_vehicules, name="test3"),
    #path('detail/<int:vehicule_id>/', views.detail_vehicule, name='detail_vehicule'),
    path('vehicule/<slug:slug>/', views.detail_vehicule, name='detail_vehicule'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('info_affectation_versement/<int:affectation_id>/', views.info_affectation_versement, name='info_affectation_versement'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)