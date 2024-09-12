from flask import render_template, request, redirect, url_for, flash, Blueprint
from models import db, Candidature, Vote
# from __main__ import app
import config
from utils import hash, valider_matricule_candidat, valider_matricule_votant


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

        if not valider_matricule_candidat(matricule, poste):
            flash("Votre matricule n'est pas autorisé pour ce poste.", 'error')
            return redirect(url_for('templates.candidature'))

        # s'assurer qu'il n'y pas pas deja une candidature existante à ce poste pour ce matricule

        candidature_existante = Candidature.query.filter_by(matricule=matricule, poste=poste).first() 
        if candidature_existante:
            flash("Ce matricule a déjà deposé une candidature pour ce poste.", 'error')
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

        if not valider_matricule_votant(matricule, poste):
            flash("Vous n'êtes pas autorisé à voter.", 'error')
            return redirect(url_for('templates.vote', poste=poste))
            
        
        ip_hash = hash(request.remote_addr)
        ip_vote_existant = Vote.query.filter_by(poste=poste, ip_hash=ip_hash).first()

        matricule_hash = hash(matricule)
        matricule_vote_existant = Vote.query.filter_by(poste=poste, matricule_hash=matricule_hash).first()

        if ip_vote_existant or matricule_vote_existant:
            flash("Vous avez déjà voté pour ce poste.\n Si vous continuez, on risque vous ban !", 'error')
        else:
            nouveau_vote = Vote(poste=poste, candidat_id=candidat_id, ip_hash=ip_hash, matricule_hash=matricule_hash)
            db.session.add(nouveau_vote)
            db.session.commit()
            flash('Votre vote a été enregistré avec succès!', 'success')

        return redirect(url_for('templates.home'))

    candidats = Candidature.query.filter_by(poste=poste).all()
    return render_template('vote.html', poste=poste, poste_texte=config.POSTES[poste], candidats=candidats)