# Microservice FastAPI

## Rôle
Mini application web Python qui simule un vrai microservice en production.
Son rôle principal est d'exposer des métriques RED (Rate, Errors, Duration)
que Prometheus vient scraper toutes les 15 secondes.

## Fichiers

| Fichier | Rôle |
|---------|------|
| `main.py` | Code source de l'application FastAPI |
| `requirements.txt` | Dépendances Python |
| `Dockerfile` | Instructions de construction de l'image Docker |

## Endpoints

| Endpoint | Rôle |
|----------|------|
| `/` | Requête normale — simule un traitement rapide (10ms à 500ms) |
| `/slow` | Requête lente — simule un traitement coûteux (1s à 3s) |
| `/error` | Génère des erreurs aléatoires (30% du temps) |
| `/health` | Vérifie que le service est vivant |
| `/metrics` | Exposé à Prometheus — retourne les métriques RED |

## Métriques RED

| Métrique | Type | Description |
|----------|------|-------------|
| `http_requests_total` | Counter | Nombre total de requêtes — **Rate** |
| `http_errors_total` | Counter | Nombre total d'erreurs — **Errors** |
| `http_request_duration_seconds` | Histogram | Temps de réponse — **Duration** |

## Tester manuellement

```bash
# Appeler les endpoints
curl http://localhost:8000/
curl http://localhost:8000/slow
curl http://localhost:8000/error
curl http://localhost:8000/health

# Voir les métriques brutes
curl http://localhost:8000/metrics

# Générer du trafic pour remplir les dashboards
for i in $(seq 1 50); do
  curl -s http://localhost:8000/ > /dev/null
  curl -s http://localhost:8000/error > /dev/null
done
```

## Port
Le microservice écoute sur le port `8000`.
