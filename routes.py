from flask import render_template, request, redirect, url_for, flash, Blueprint
from models import db, Candidature, Vote
# from __main__ import app
import config
from utils import hash_ip, validate_matricule


router = Blueprint("templates",__name__)

@router.route('/')
def home():
    return render_template('home.html', postes=config.POSTES)

@router.route('/candidature', methods=['GET', 'POST'])
def candidature():
    if request.method == 'POST':
        matricule = request.form['matricule']
        poste = request.form['poste']
        nom = request.form['nom']
        programme = request.form['programme']

        if not validate_matricule(matricule, poste):
            flash("Votre matricule n'est pas autorisé pour ce poste.", 'error')
            return redirect(url_for('templates.candidature'))

        nouvelle_candidature = Candidature(matricule=matricule, poste=poste, nom=nom, programme=programme)
        db.session.add(nouvelle_candidature)
        db.session.commit()
        flash('Votre candidature a été enregistrée avec succès!', 'success')
        return redirect(url_for('templates.home'))

    return render_template('candidature.html', postes=config.POSTES)

@router.route('/vote/<poste>', methods=['GET', 'POST'])
def vote(poste):
    if request.method == 'POST':
        matricule = request.form['matricule']
        candidat_id = request.form['candidat_id']

        if matricule not in config.MATRICULES_VOTANTS:
            flash("Vous n'êtes pas autorisé à voter.", 'error')
            return redirect(url_for('templates.vote', poste=poste))

        ip_hash = hash_ip(request.remote_addr)
        vote_existant = Vote.query.filter_by(poste=poste, ip_hash=ip_hash).first()

        if vote_existant:
            flash("Vous avez déjà voté pour ce poste.", 'error')
        else:
            nouveau_vote = Vote(poste=poste, candidat_id=candidat_id, ip_hash=ip_hash)
            db.session.add(nouveau_vote)
            db.session.commit()
            flash('Votre vote a été enregistré avec succès!', 'success')

        return redirect(url_for('templates.home'))

    candidats = Candidature.query.filter_by(poste=poste).all()
    return render_template('vote.html', poste=poste, candidats=candidats)