import hashlib
import os
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from models import db, Candidature, Vote
# from __main__ import app
import config
from config import POSTES, UPLOAD_FOLDER
from utils import hash, valider_matricule_candidat, valider_matricule_votant

from datetime import timedelta
import json

router = Blueprint("templates", __name__)


@router.route('/')
def home():
    return render_template('home.html', postes=config.POSTES, POSTES=config.POSTES)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@router.route('/candidature', methods=['GET', 'POST'])
def candidature():
    if request.method == 'POST':
        matricule = request.form.get('matricule').upper()
        poste = request.form.get('poste')
        nom = request.form.get('nom')

        # Vérifications de base
        if not all([matricule, poste, nom]):
            flash("Tous les champs obligatoires doivent être remplis.", 'error')
            return redirect(url_for('templates.candidature'))

        if not valider_matricule_candidat(matricule, poste):
            flash("Votre matricule n'est pas autorisé pour ce poste.", 'error')
            return redirect(url_for('templates.candidature'))

        # # Vérification de l'existence d'une candidature
        # candidature_existante = Candidature.query.filter_by(
        #     matricule=matricule, poste=poste).first()
        # if candidature_existante:
        #     flash("Ce matricule a déjà déposé une candidature pour ce poste.", 'info')
        #     return redirect(url_for('templates.home'))

        # FIX: Corrige l'erreur de double postulation
        candidatures = Candidature.query.filter_by(matricule=matricule).all()
        for candidature in candidatures:
            if candidature.poste == poste:
                # candidature existante
                flash(
                    "Ce matricule a déjà déposé une candidature pour ce poste.", 'info')
                return redirect(url_for('templates.home'))

            if candidature.nom == nom:
                flash(
                    f"Le nom {candidature.nom} a été detecté pour ce matricule, il sera utilisé", 'info')
                return redirect(url_for('templates.home'))

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

        # Création de la nouvelle candidature
        nouvelle_candidature = Candidature(
            matricule=matricule,
            poste=poste,
            nom=nom,
            photo=photo_filename,
            programme=programme_filename,
            description=description
        )

        try:
            db.session.add(nouvelle_candidature)
            db.session.commit()
            flash('Votre candidature a été enregistrée avec succès!', 'success')
            return redirect(url_for('templates.home'))
        except Exception as e:
            db.session.rollback()
            flash(
                f'Une erreur est survenue lors de l\'enregistrement de votre candidature: {str(e)}', 'error')
            return redirect(url_for('templates.candidature'))

    return render_template('candidature.html', postes=POSTES)


@router.route('/vote/<poste>', methods=['GET', 'POST'])
def vote(poste):
    if poste not in config.POSTES:
        flash("Poste invalide.", 'error')
        return redirect(url_for('templates.home'))

    if request.method == 'POST':
        matricule = request.form.get('matricule').upper()
        candidat_id = request.form.get('candidat_id')

        if not matricule or not candidat_id:
            flash("Veuillez remplir tous les champs.", 'error')
            return redirect(url_for('templates.vote', poste=poste))

        if not valider_matricule_votant(matricule, poste):
            flash("Vous n'êtes pas autorisé à voter pour ce poste.", 'error')
            return redirect(url_for('templates.vote', poste=poste))

        # ip_hash = hashlib.sha256(request.remote_addr.encode()).hexdigest()
        matricule_hash = hashlib.sha256(matricule.encode()).hexdigest()

        # ip_vote_existant = Vote.query.filter_by(poste=poste, ip_hash=ip_hash).first()
        # matricule_vote_existant = Vote.query.filter_by(poste=poste, matricule_hash=matricule_hash).first()

        # if ip_vote_existant or matricule_vote_existant:
        #     flash("Vous avez déjà voté pour ce poste. Si vous continuez, vous risquez d'être banni !", 'warning')
        #     return redirect(url_for('templates.vote', poste=poste))

        # [FIX]: empecher un candidat de voter
        candidat = Candidature.query.filter_by(id=candidat_id).first()
        if matricule == candidat.matricule:
            flash("Vous avez postulé, donc ne pouvez pas voter.", 'error')
            return redirect(url_for('templates.vote', poste=poste))

        try:
            nouveau_vote = Vote(
                poste=poste, candidat_id=candidat_id, matricule_hash=matricule_hash)
            db.session.add(nouveau_vote)
            db.session.commit()
            flash('Votre vote a été enregistré avec succès!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(
                f"Une erreur est survenue lors de l'enregistrement de votre vote : {str(e)}", 'error')

        return redirect(url_for('templates.home'))

    candidats = Candidature.query.filter_by(poste=poste).all()
    return render_template('vote.html', poste=poste, poste_texte=config.POSTES[poste], candidats=candidats)


@router.route('/resultats', methods=['GET'])
def resultats():
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

    return render_template("resultats.html", POSTES=POSTES, resultats=resultats)
