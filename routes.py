import hashlib
import os
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from models import db, Candidature, Vote
# from __main__ import app
import config
from config import POSTES, UPLOAD_FOLDER, get_phase, SECU
from utils import hash, valider_matricule_candidat, valider_matricule_votant
import socket

from datetime import datetime
import json

router = Blueprint("templates", __name__)


@router.route('/delete_candidature', methods=['GET', 'POST'])
def delete_candidature():
    if request.method == 'POST':
        print("Posting")
        matricule = request.form.get("matricule").upper().strip()
        poste = request.form.get("poste")
        _secu = request.form.get("secu")

        secu = hashlib.sha256(_secu.encode()).hexdigest()

        if secu != SECU:
            flash("Mauvaise sécurité. Vous n'avez pas les droits pour cela.")

        # faire une requette pour supprimer la candidature en question
        candidature = Candidature.query.filter_by(poste=poste, matricule=matricule).first()
        if not candidature:
            flash(f"Cette candidature n'existe pas", "info")
            return render_template("delete_candidature.html", postes=POSTES)    
        db.session.delete(candidature)
        db.session.commit()
        flash(f"En principe, la candidature de {candidature.nom} au poste de {poste} a été supprimée ", "succes")

    return render_template("delete_candidature.html", postes=POSTES)


@router.route('/')
def home():
    now = datetime.now()
    phase = get_phase(now)
    return render_template('home.html', phase=phase, postes=config.POSTES, POSTES=config.POSTES )


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@router.route('/candidature', methods=['GET', 'POST'])
def candidature():
    now = datetime.now()
    phase = get_phase(now)
    if request.method == 'POST':
        matricule = request.form.get('matricule').upper().strip()
        poste = request.form.get('poste')
        nom = request.form.get('nom')

        # Vérifications de base
        if not all([matricule, poste, nom]):
            flash("Tous les champs obligatoires doivent être remplis.", 'error')
            return redirect(url_for('templates.candidature', phase=phase))

        if not valider_matricule_candidat(matricule, poste):
            flash("Votre matricule n'est pas autorisé pour ce poste.", 'error')
            return redirect(url_for('templates.candidature', phase=phase))

        # Vérification de l'existence d'une candidature
        candidature_existante = Candidature.query.filter_by(
            matricule=matricule).first()

        if candidature_existante and candidature_existante.nom != nom:
            flash(
                f"Le nom {candidature_existante.nom} a été trouvé pour ce matricule, il sera utilisé", 'info')
            nom = candidature_existante.nom

        # Gestion de l'upload de la photo
        if 'photo' not in request.files:
            flash('Aucune photo n\'a été fournie', 'error')
            return redirect(request.url)
        photo = request.files['photo']
        if photo.filename == '':
            flash('Aucune photo sélectionnée', 'error')
            return redirect(request.url)
        if photo and allowed_file(photo.filename):
            photo_filename = secure_filename(f"{matricule}_{photo.filename}")
            photo_save_path = os.path.join(UPLOAD_FOLDER, photo_filename)
            photo.save(photo_save_path)
        else:
            flash('Format de fichier non autorisé pour la photo', 'error')
            return redirect(request.url)

        # Gestion de l'upload du programme (pour les présidents) ou de la description
        programme_filename = None
        description = None
        if poste == 'president':
            if 'programme' not in request.files:
                flash('Aucun programme n\'a été fourni', 'error')
                return redirect(request.url)
            programme = request.files['programme']
            if programme.filename == '':
                flash('Aucun programme sélectionné', 'error')
                return redirect(request.url)
            if programme and allowed_file(programme.filename):
                programme_filename = secure_filename(
                    f"{matricule}_{programme.filename}")
                programme_save_path = os.path.join(
                    UPLOAD_FOLDER, programme_filename)
                programme.save(programme_save_path)
            else:
                flash('Format de fichier non autorisé pour le programme', 'error')
                return redirect(request.url)
        else:
            description = request.form.get('description')
            if not description:
                flash('La description/vision est obligatoire pour ce poste', 'error')
                return redirect(request.url)

        try:
            if candidature_existante:
                # Mise à jour de la candidature existante
                candidature_existante.poste = poste
                candidature_existante.nom = nom
                candidature_existante.photo = photo_filename
                candidature_existante.programme = programme_filename
                candidature_existante.description = description
                db.session.commit()
                flash('Votre candidature a été mise à jour avec succès!', 'success')
            else:
                # Création d'une nouvelle candidature
                nouvelle_candidature = Candidature(
                    matricule=matricule,
                    poste=poste,
                    nom=nom,
                    photo=photo_filename,
                    programme=programme_filename,
                    description=description
                )
                db.session.add(nouvelle_candidature)
                db.session.commit()
                flash('Votre candidature a été enregistrée avec succès!', 'success')

            return redirect(url_for('templates.home'))
        except Exception as e:
            db.session.rollback()
            flash(
                f'Une erreur est survenue lors de l\'enregistrement de votre candidature: {str(e)}', 'error')
            return redirect(url_for('templates.candidature'))

    return render_template('candidature.html', postes=POSTES, phase=phase)

from flask import request, redirect, url_for, flash, render_template, make_response
import hashlib
from datetime import datetime, timedelta

@router.route('/vote/<poste>', methods=['GET', 'POST'])
def vote(poste):
    now = datetime.now()
    phase = get_phase(now)

    if poste not in config.POSTES:
        flash("Poste invalide.", 'error')
        return redirect(url_for('templates.home'))

    if request.method == 'POST' and request.headers and request.remote_addr:


        matricule = request.form.get('matricule', '').upper().strip()
        candidat_id = request.form.get('candidat_id')

        if not matricule or not candidat_id:
            flash("Veuillez remplir tous les champs.", 'error')
            return redirect(url_for('templates.vote', poste=poste))

        # Crée un hash pour le matricule
        matricule_hash = hashlib.sha256(matricule.encode()).hexdigest()

        # Vérifie si l'utilisateur a déjà voté (via cookie ou IP)
        if request.cookies.get(f'vote_{poste}') or \
                Vote.query.filter_by(poste=poste, matricule_hash=matricule_hash).first():
            flash("Vous avez déjà voté pour ce poste.", 'warning')
            return redirect(url_for('templates.vote', poste=poste))

        # Empêcher un candidat de voter pour lui-même
        candidat = Candidature.query.filter_by(id=candidat_id).first()
        if candidat and candidat.matricule == matricule:
            flash("Vous ne pouvez pas voter pour vous-même.", 'error')
            return redirect(url_for('templates.vote', poste=poste))

        try:
            # Enregistrement du vote dans la base de données
            nouveau_vote = Vote(poste=poste, candidat_id=candidat_id, matricule_hash=matricule_hash)
            db.session.add(nouveau_vote)
            db.session.commit()

            # Crée un cookie pour bloquer de futurs votes depuis cet appareil
            response = make_response(redirect(url_for('templates.home')))
            response.set_cookie(f'vote_{poste}', '1', max_age=3600*24, httponly=True)

            flash("Votre vote a été enregistré avec succès!", 'success')
            return response

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'enregistrement du vote : {str(e)}", 'error')

    candidats = Candidature.query.filter_by(poste=poste).all()
    return render_template('vote.html', poste=poste, phase=phase, candidats=candidats, poste_texte=config.POSTES[poste])



@router.route('/resultats', methods=['GET'])
def resultats():
    now = datetime.now()
    phase = get_phase(now)
    resultats = dict()
    for poste in POSTES.keys():
        candidatures = Candidature.query.filter_by(poste=poste).all()
        total_votes_number = Vote.query.filter_by(poste=poste).count() or 1

        resultats[poste] = dict()

        for candidate in candidatures:
            candidate_votes_number = Vote.query.filter_by(
                poste=poste, candidat_id=candidate.id).count()
            pourcentage = round(
                (candidate_votes_number * 100 / total_votes_number), 1)
            resultats[poste][candidate.nom] = pourcentage

    return render_template("resultats.html", phase=phase, POSTES=POSTES, resultats=resultats)
