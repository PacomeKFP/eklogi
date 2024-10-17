from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Fingerprint(db.Model):
    __tablename__ = 'fingerprint'
    id = db.Column(db.Integer, primary_key=True)
    user_agent = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship('Client', back_populates='fingerprint', uselist=False)

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    candidature_id = db.Column(db.Integer, db.ForeignKey('candidature.id'), nullable=False)
    fingerprint_id = db.Column(db.Integer, db.ForeignKey('fingerprint.id'), unique=True, nullable=False)
    matricule = db.Column(db.String(8), nullable=False, unique=True)

    fingerprint = db.relationship('Fingerprint', back_populates='client', uselist=False)

class Candidature(db.Model):
    __tablename__ = 'candidature'
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(8), nullable=False)
    poste = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    programme = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)

class Vote(db.Model):
    __tablename__ = 'vote'
    id = db.Column(db.Integer, primary_key=True)
    poste = db.Column(db.String(50), nullable=False)
    candidat_id = db.Column(db.Integer, db.ForeignKey('candidature.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
