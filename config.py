# Configuration des postes disponibles
POSTES = {
    'president': 'Président',
    'vice_president': 'Vice-président',
    'secretaire': 'Secrétaire',
    'tresorier': 'Trésorier'
}

# Matricules autorisés à voter (exemple)
MATRICULES_VOTANTS = [
    '20210001', '20210002', '20210003', '20210004', '20210005',
    '20220001', '20220002', '20220003', '20220004', '20220005'
]

# Types de matricules autorisés par poste (exemple)
MATRICULES_PAR_POSTE = {
    'president': ['21', '20'],  # Matricules commençant par 2021 ou 2022
    'vice_president': ['21', '20'],
    'secretaire': ['21', '20'],
    'tresorier': ['21', '20']
}

# Configuration de la base de données
DATABASE_URI = 'sqlite:///elections.db'

# Clé secrète pour la session Flask
SECRET_KEY = 'votre_cle_secrete_ici'  # À changer en production !