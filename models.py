from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Candidature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(8), nullable=False)
    poste = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(255), nullable=False)  # Chemin de la photo
    programme = db.Column(db.String(255), nullable=True)  # Chemin du fichier PDF pour les présidents
    description = db.Column(db.Text, nullable=True)  # Pour les autres postes

# Modèle de vote
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poste = db.Column(db.String(50), nullable=False)
    candidat_id = db.Column(db.Integer, db.ForeignKey('candidature.id'), nullable=False)
    ip_hash = db.Column(db.String(64), nullable=False)
    matricule_hash = db.Column(db.String(64), nullable=False)

