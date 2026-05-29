# Image de base Python légère
FROM python:3.12-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Copie et installe les dépendances en premier
# (optimisation Docker : cette couche est mise en cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source
COPY main.py .

# Port sur lequel FastAPI écoute
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
