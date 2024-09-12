import hashlib
import config
import logging

_logger = logging.getLogger(__name__)

from models import Candidature


def hash(string:str):
    return hashlib.sha256(string.encode()).hexdigest()

def validate_matricule(matricule, poste):


    if not poste and matricule not in config.MATRICULES_VOTANTS:
        return False
    
    prefix = matricule[:2]  # Les 4 premiers chiffres du matricule
    return prefix in config.MATRICULES_PAR_POSTE.get(poste, [])

def valider_matricule_candidat(matricule, poste):
    # il faut etre dans la liste des matricules de 4GI ()
    if "adjoint" in poste and matricule not in config.MATRICULES_3GI:
        return False
    
    if matricule not in config.MATRICULES_4GI:
        return False
    
    # TODO: s'assurer que le candidat n'a pas encore gagné les elections d'un autre truc

    return True

def valider_matricule_votant(matricule, poste):
    # il ne doit pas etre candidat au poste

    candidature_existante = Candidature.query.filter_by(poste=poste, matricule=matricule).first()
    if candidature_existante:
        _logger.warning("Il est candidat")
        return False


    # il doit etre soit un 4GI soit un 3GI
    if matricule not in [*config.MATRICULES_3GI, *config.MATRICULES_4GI]:
        _logger.warning("Probleme de matricule")
        return False
    
    return True