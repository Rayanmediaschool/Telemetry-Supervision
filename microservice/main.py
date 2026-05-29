import time
import random
from fastapi import FastAPI, Response
from prometheus_client import (
    Counter,         # Compteur qui ne fait qu'augmenter
    Histogram,       # Distribution de valeurs (temps de réponse)
    generate_latest  # Génère le texte au format Prometheus
)

app = FastAPI()

# ── MÉTRIQUES RED ─────────────────────────────────────────

# RATE : nombre total de requêtes reçues
# labels = on peut filtrer par endpoint et code HTTP
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Nombre total de requêtes HTTP reçues',
    ['method', 'endpoint', 'status_code']
)

# ERRORS : nombre de requêtes en erreur
ERROR_COUNT = Counter(
    'http_errors_total',
    'Nombre total de requêtes en erreur',
    ['method', 'endpoint']
)

# DURATION : temps de réponse en secondes
# Les buckets définissent les tranches de mesure
REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'Durée des requêtes HTTP en secondes',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
)

# ── ENDPOINTS ─────────────────────────────────────────────

@app.get("/")
def root():
    """Endpoint principal — simule un traitement normal"""
    start = time.time()

    # Simule un temps de traitement aléatoire (10ms à 500ms)
    time.sleep(random.uniform(0.01, 0.5))

    duration = time.time() - start
    REQUEST_COUNT.labels(method="GET", endpoint="/", status_code="200").inc()
    REQUEST_DURATION.labels(method="GET", endpoint="/").observe(duration)

    return {"status": "ok", "message": "Microservice operationnel"}


@app.get("/slow")
def slow():
    """Endpoint lent — simule une opération coûteuse"""
    start = time.time()

    # Simule un traitement long (1s à 3s)
    time.sleep(random.uniform(1.0, 3.0))

    duration = time.time() - start
    REQUEST_COUNT.labels(method="GET", endpoint="/slow", status_code="200").inc()
    REQUEST_DURATION.labels(method="GET", endpoint="/slow").observe(duration)

    return {"status": "ok", "message": "Traitement lent termine"}


@app.get("/error")
def error():
    """Endpoint qui génère aléatoirement des erreurs (30% du temps)"""
    start = time.time()

    if random.random() < 0.3:
        # 30% de chance d'erreur
        duration = time.time() - start
        REQUEST_COUNT.labels(method="GET", endpoint="/error", status_code="500").inc()
        ERROR_COUNT.labels(method="GET", endpoint="/error").inc()
        REQUEST_DURATION.labels(method="GET", endpoint="/error").observe(duration)
        return Response(
            content='{"status": "error", "message": "Erreur simulee"}',
            status_code=500,
            media_type="application/json"
        )

    duration = time.time() - start
    REQUEST_COUNT.labels(method="GET", endpoint="/error", status_code="200").inc()
    REQUEST_DURATION.labels(method="GET", endpoint="/error").observe(duration)
    return {"status": "ok", "message": "Pas d erreur cette fois"}


@app.get("/health")
def health():
    """Endpoint de santé — vérifie que le service est vivant"""
    REQUEST_COUNT.labels(method="GET", endpoint="/health", status_code="200").inc()
    return {"status": "healthy"}


@app.get("/metrics")
def metrics():
    """
    Endpoint scrappé par Prometheus toutes les 15 secondes.
    Retourne toutes les métriques RED au format texte Prometheus.
    """
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
