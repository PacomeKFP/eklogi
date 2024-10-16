# Utiliser une image de base Python officielle
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application
COPY . .

# Exposer le port sur lequel l'application s'exécute
EXPOSE 5000

# Définir la variable d'environnement pour Flask
ENV FLASK_APP=app.py

# Définir la variable d'environnement pour le mode production ou développement
# Par exemple : 'development' pour le mode développement, 'production' pour production
ENV FLASK_ENV=development

# Commande pour exécuter l'application
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
