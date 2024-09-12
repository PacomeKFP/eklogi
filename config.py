# Configuration des postes disponibles
POSTES = {
    'president': 'Président(e)',
    'president_adjoint': 'Vice-président(e)',
    'secretaire': 'Secrétaire Général',
    'secretaire_adjoint': 'Secrétaire Adjoint(e)',
    'tresorier': 'Trésorier(e)',
    'tresorier_adjoint': "Trésorier(e) Adjoint(e)",
    'chef_cellule_projet': "Chef(fe) Cellule Projet",
    'adjoint_cellule_projet': "Adjoint(e) Cellule Projet",
    'chef_cellule_communication': "Chef(fe) Cellule Communication",
    'adjoint_cellule_communication': "Chef(fe) Cellule Communication",
}

# Matricules autorisés à voter (exemple)
MATRICULES_VOTANTS = [
    '20210001', '20210002', '20210003', '20210004', '20210005',
    '20220001', '20220002', '20220003', '20220004', '20220005'
]

# Types de matricules autorisés par poste (exemple)
MATRICULES_PAR_POSTE = {
    'president': ['21', '20'],  # Matricules commençant par 2021 ou 2022
    'president_adjoint': ['21', '20'],
    'secretaire': ['21', '20'],
    'secretaire_adjoint': ['21', '20'],
    'tresorier': ['21', '20'],
    'tresorier_adjoint': ['21', '20'],
    'chef_cellule_projet': ['21', '20'],
    'adjoint_cellule_projet': ['21', '20'],
    'chef_cellule_communication': ['21', '20'],
    'adjoint_cellule_communication': ['21', '20'],
}

PHASES = [
    1, # Phase de candidature
    2, # Phase des elections se decline en autant d'etapes qu'il y a de postes
    3  # Phase de Consultation des resultats, une fois la phase 2 terminée 
]

# TODO: changer les matricules par les matricules réels
MATRICULES_3GI= [f"22P{'%03d'%i}" for i in range(600)]
MATRICULES_4GI= [f"21P{'%03d'%i}" for i in range(500)]

# Configuration de la base de données
DATABASE_URI = 'sqlite:///elections.db'

# Clé secrète pour la session Flask
SECRET_KEY = 'votre_cle_secrete_ici'  # À changer en production !

