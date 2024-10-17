from datetime import datetime, date
import hashlib
import pytz

# DATABASE_URI = 'mysql://root:root_password@localhost:3306/eklogi'   # for MySQL
DATABASE_URI = 'sqlite:///elections.db' # for sqlite



# Configuration des postes disponibles
POSTES = {
    'president': 'Président(e)',
    'secretaire': 'Secrétaire Général(e)',
    'tresorier': 'Trésorier(e)',
    'chef_cellule_projet': "Chef(fe) Cellule Projet",
    'chef_cellule_communication': "Chef(fe) Cellule Communication",
    'chef_cellule_relation_exterieures': "Chef(fe) Cellule Relations Exterieures",

    'president_adjoint': 'Vice-président(e)',
    'secretaire_adjoint': 'Secrétaire Adjoint(e)',
    'tresorier_adjoint': "Trésorier(e) Adjoint(e)",
    'adjoint_cellule_projet': "Adjoint(e) Cellule Projet",
    'adjoint_cellule_communication': "Adjoint(e) Cellule Communication",
    'adjoint_cellule_relation_exterieures': "Adjoint(e) Cellule Relations Exterieures",
}

UPLOAD_FOLDER = "uploads"

cameroun_tz = pytz.timezone('Africa/Douala')

# Phases avec fuseau horaire du Cameroun
PHASES = {
    "candidatures": (
        cameroun_tz.localize(datetime(2024, 10, 7, 0, 0, 0, 1)),
        cameroun_tz.localize(datetime(2024, 10, 16, 0, 0, 0, 1)),
    ),
    "votes": (
        cameroun_tz.localize(datetime(2024, 10, 16, 0, 0, 0, 2)),
        cameroun_tz.localize(datetime(2024, 10, 16, 17, 0, 0, 1)),
    ),
}


def get_phase(current_date: datetime):
    current_date = cameroun_tz.fromutc(current_date)  # Assure que la date est dans le fuseau horaire Cameroun

    if current_date <= PHASES['candidatures'][0]:
        return 0  # Pas encore lancé
    if PHASES['candidatures'][0] <= current_date <= PHASES['candidatures'][1]:
        return 1  # phase de candidature
    if PHASES['votes'][0] <= current_date <= PHASES['votes'][1]:
        return 2  # Phase de votes

    return 3  # Phase de résultats



# Matricules autorisés à voter (exemple)
MATRICULES_3GI = ["22P001","22P612", "22P265", "22P340", "22P508", "22P601", "22P590", "22P517", "22P206", "22P448", "22P541", "22P600", "22P283", "22P236", "21P358", "22P195", "22P232", "22P221", "22P207", "22P279", "22P274", "22P230", "22P359", "21P247", "20P216", "22P294", "22P539", "22P334", "22P231", "22P295", "22P526", "22P509", "22P223", "22P405", "22P267", "22P594", "22P585", "22P372", "22P224", "22P216", "22P371", "22P495", "22P557", "22P217", "22P380", "22P306", "22P214", "22P544", "22P341", "22P581", "22P525", "22P260", "21P200", "22P226", "22P482", "22P292", "22P204", "22P596", "22P261", "22P239", "22P277", "22P368", "22P248", "22P327", "22P584", "22P569", "22P533", "22P607", "22P582",
                  "22P250", "22P587", "22P325", "22P437", "21P064", "22P540", "22P235", "21P191", "22P486", "22P309", "22P344", "22P229", "22P352", "22P256", "22P572", "22P215", "22P238", "22P245", "22P523", "22P333", "22P456", "22P227", "22P608", "22P387", "22P506", "22P284", "22P345", "22P563", "22P278", "22P529", "22P513", "22P389", "22P446", "22P211", "22P246", "22P609", "22P362", "21P045", "22P218", "24P750", "24P751", "24P764", "24P765", "21P103", "21P266", "21P124", "21P068", "21P040", "21P398", "24P752", "24P766", "21P023", "24P753", "24P754", "21P017", "24P755", "17P025", "21P341", "24P756", "24P749", "24P767", "14P757", "19P070", "24P758", "24P759", "20P151", "24P760", "24P761", "24P762", "21P339"]

MATRICULES_4GI = ['21P001', '21P187', '21P296', '21P372', '21P021', '21P027', '21P149', '21P340', '21P272', '21P223', '21P360', '21P082', '21P233', '21P169', '21P279', '21P336', '21P038', '19P162', '21P262', '21P127', '21P344', '21P107', '21P274', '21P287', '21P039', '21P172', '21P011', '21P320', '20P292', '21P275', '20P200', '21P070', '21P014', '21P034', '20P239', '21P269', '20P094', '21P254', '21P369', '21P072', '21P335', '21P130', '23P751',
                  '21P278', '21P356', '21P240', '23P797', '23P752', '22P142', '21P089', '21P318', '21P012', '21P110', '20P231', '18P156', '23P770', '23P756', '21P273', '21P188', '21P228', '21P073', '21P308', '21P284', '21P093', '21P190', '21P033', '21P246', '21P050', '21P061', '23P753', '21P301', '21P024', '23P750', '20P147', '21P156', '20P286', '21P081', '21P373', '21P086', '21P382', '21P091', '21P417', '21P128', '21P030', '21P018', '19P300', '21P174']


# Configuration de la base de données

# Clé secrète pour la session Flask
SECRET_KEY = 'votre_cle_secrete_ici'  # À changer en production !
SECU = "d7eec39d2c2cbd8c7c12ccf1f31a25755db8653380c9e69a7b2d6d8b93449333"
