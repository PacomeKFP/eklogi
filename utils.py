import hashlib
import config
import logging
from flask import flash

_logger = logging.getLogger(__name__)

from models import Candidature


def hash(string:str):
    return hashlib.sha256(string.encode()).hexdigest()





def valider_matricule_candidat(matricule, poste):
    print(matricule)
    # il doit etre soit un 4GI soit un 3GI
    if matricule not in [*config.MATRICULES_3GI, *config.MATRICULES_4GI]:
        flash("Votre matricule ne correspond pas à celui d'un etudiant de 3eme ou de 4eme année du GI", "info")
        return False


    # il faut etre dans la liste des matricules de 4GI ()
    if ("adjoint" in poste) and (matricule not in config.MATRICULES_3GI):
        flash("Seuls les etudiants de 3eme année peuvent postuler au poste d'adjoint ou vice", "info")
        return False
    
    elif "adjoint" not in poste and matricule not in config.MATRICULES_4GI:
        flash("Seuls les etudiant de 4eme année peuvent postuler aux postes de Chef ou Président", "info")
        return False
    
    # TODO: s'assurer que le candidat n'a pas encore gagné les elections d'un autre truc

    return True

def valider_matricule_votant(matricule, poste):
    # il ne doit pas etre candidat au poste

    candidature_existante = Candidature.query.filter_by(poste=poste, matricule=matricule).first()
    if candidature_existante:
        flash("Vous etes candidat à ce poste, donc vous ne pouvez pas voter pour le poste", "info")
        return False

    print(matricule)

    # il doit etre soit un 4GI soit un 3GI
    if matricule not in [*config.MATRICULES_3GI, *config.MATRICULES_4GI]:
        flash("Il semblerait que votre matricule ne soit pas celui d'un étudiant de 3eme ou 4eme année GI", "info")
        return False
    
    return True