import hashlib
import config

def hash_ip(ip):
    return hashlib.sha256(ip.encode()).hexdigest()

def validate_matricule(matricule, poste):
    if not poste and matricule not in config.MATRICULES_VOTANTS:
        return False
    
    prefix = matricule[:2]  # Les 4 premiers chiffres du matricule
    return prefix in config.MATRICULES_PAR_POSTE.get(poste, [])