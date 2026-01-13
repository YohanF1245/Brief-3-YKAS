import pandera.pandas as pa
from pandera.typing import Series
from datetime import datetime

# --- 1. Schéma Opérations ---
class OperationsSchema(pa.DataFrameModel):
    operation_id: Series[int] = pa.Field(unique=True, description="ID unique de l'opération")
    type_operation: Series[str] = pa.Field(nullable=True, isin=["SAR", "MAS", "DIV"], description="Type d'opération (Search And Rescue, etc.)")
    pourquoi_alerte: Series[str] = pa.Field(nullable=True)
    moyen_alerte: Series[str]
    # Validation géographique
    latitude: Series[float] = pa.Field(nullable=True, ge=-90, le=90)
    longitude: Series[float] = pa.Field(nullable=True, ge=-180, le=180)
    # Dates
    date_heure_reception_alerte: Series[datetime]
    date_heure_fin_operation: Series[datetime]

    class Config:
        coerce = True
        strict = False

# --- 2. Schéma Flotteurs ---
class FlotteursSchema(pa.DataFrameModel):
    operation_id: Series[int]
    numero_ordre: Series[int]
    type_flotteur: Series[str] = pa.Field(str_matches=r"^[a-zA-Z0-9\s]+$")
    
    class Config:
        coerce = True

# --- 3. Schéma Résultats Humains ---
class ResultatsHumainSchema(pa.DataFrameModel):
    operation_id: Series[int]
    categorie_personne: Series[str]
    resultat_humain: Series[str]
    nombre: Series[int] = pa.Field(ge=0)
    dont_nombre_blesse: Series[int] = pa.Field(ge=0)

    class Config:
        coerce = True
        
# --- 4. Schéma Opérations Stats ---
class OperationsStatsSchema(pa.DataFrameModel):
    operation_id: Series[int] = pa.Field(unique=True, description="Clé primaire")
    date: Series[datetime]
    
    annee: Series[int] = pa.Field(ge=1900, le=2100)
    mois: Series[int] = pa.Field(ge=1, le=12)
    jour: Series[int] = pa.Field(ge=1, le=31)
    
    mois_texte: Series[str] = pa.Field(isin=[
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
    ])
    jour_semaine: Series[str] = pa.Field(isin=[
        'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'
    ])
    phase_journee: Series[str] = pa.Field(nullable=True, isin=[
        'matinée', 'déjeuner', 'après-midi', 'nuit'
    ])
    
    est_weekend: Series[bool]
    est_jour_ferie: Series[bool]
    concerne_plongee: Series[bool]
    
    # Données géographiques/physiques
    distance_cote_milles_nautiques: Series[float] = pa.Field(nullable=True, ge=0)
    maree_coefficient: Series[int] = pa.Field(nullable=True, ge=20, le=120)
    
    # Statistiques
    nombre_personnes_blessees: Series[int] = pa.Field(ge=0)
    nombre_personnes_assistees: Series[int] = pa.Field(ge=0)
    nombre_personnes_decedees: Series[int] = pa.Field(ge=0)
    nombre_personnes_disparues: Series[int] = pa.Field(ge=0)
    nombre_personnes_secourues: Series[int] = pa.Field(ge=0)
    nombre_personnes_impliquees: Series[int] = pa.Field(ge=0)
    
    nombre_flotteurs_plaisance_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_commerce_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_peche_impliques: Series[int] = pa.Field(ge=0)

    class Config:
        coerce = True 
        strict = False