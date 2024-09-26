from datetime import datetime, date

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
PHASES = {
    "candidatures": (datetime(2024, 9, 25, 0, 0, 0, 1), datetime(2024, 10, 9, 14, 30, 0, 1)), 
    "votes": (datetime(2024, 10, 9, 14, 30, 0, 2), datetime(2024, 10, 9, 15, 30, 0, 1)), 
}
def get_phase(date: date):
    if date <= PHASES['candidatures'][0]:
        return 0 # Pas encore lancé
    if PHASES['candidatures'][0] <= date <= PHASES['candidatures'][1]:
        return 1 # phase de candidature
    if PHASES['votes'][0] <= date <= PHASES['votes'][1]:
        return 2 # Phase de votes

    return 3     # Phase de resultats


# TODO: changer les matricules par les matricules réels
MATRICULES_3GI= [f"22P{'%03d'%i}" for i in range(600)]
MATRICULES_4GI= [f"21P{'%03d'%i}" for i in range(500)]

# Configuration de la base de données
# DATABASE_URI = 'sqlite:///elections.db' # for sqlite
DATABASE_URI = 'mysql://root:root_password@localhost/db_name'   # for MySQL

# Clé secrète pour la session Flask
SECRET_KEY = 'votre_cle_secrete_ici'  # À changer en production !

