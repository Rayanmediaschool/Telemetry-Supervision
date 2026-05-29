# Image de base Python légère
FROM python:3.12-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Installe les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le script
COPY simulator.py .

# Lance le simulateur
CMD ["python", "simulator.py"]
