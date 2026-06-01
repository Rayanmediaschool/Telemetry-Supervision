# Système de supervision de télémétrie

Projet Master 1 — Informatique / Systèmes embarqués  

## Présentation

Plateforme de supervision de télémétrie multi-domaines basée sur des outils open-source.  
Elle collecte, stocke, visualise et alerte sur les métriques de trois domaines :

- **Infrastructure** — métriques système Linux et conteneurs Docker
- **IoT** — capteurs simulés (température, pression, vibration, batterie) via MQTT
- **Applicatif** — microservice FastAPI instrumenté avec la méthode RED

## Architecture
```

Capteurs IoT (simulés)
↓ MQTT
Mosquitto (broker)
↓
Telegraf (bridge MQTT → Prometheus)
↓
Prometheus (collecte + stockage TSDB 15 jours)
↓                    ↓
Alertmanager          Grafana
(routing alertes)     (dashboards)
Node Exporter → métriques Linux
cAdvisor      → métriques Docker
Microservice  → métriques RED (Rate, Errors, Duration)
Pushgateway   → métriques jobs éphémères
```

## Stack technique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| Collecte / TSDB | Prometheus | 2.54.0 |
| Alerting | Alertmanager | 0.27.0 |
| Visualisation | Grafana | 11.2.0 |
| Bridge IoT | Telegraf | 1.32 |
| Broker MQTT | Eclipse Mosquitto | 2.0 |
| Exporter OS | Node Exporter | latest |
| Exporter Docker | cAdvisor | latest |
| Microservice démo | Python 3.12 + FastAPI | 0.115.0 |
| Conteneurisation | Docker Compose | v2+ |

## Prérequis

- Docker et Docker Compose v2+
- Linux (Debian 12 recommandé)
- 4 cœurs, 8 Go RAM, 20 Go disque minimum

## Déploiement

### 1. Cloner le dépôt
```bash
git clone https://github.com/Rayanmediaschool/telemetry-supervision.git
cd telemetry-supervision
```

### 2. Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditer .env avec vos propres valeurs
```

### 3. Démarrer la plateforme
```bash
docker compose up -d
```

### 4. Vérifier que tout tourne
```bash
docker compose ps
```

## Accès aux interfaces

| Service | URL | Identifiants |
|---------|-----|--------------|
| Grafana | http://IP_VM:3000 | admin / voir .env |
| Prometheus | http://IP_VM:9090 | — |
| Alertmanager | http://IP_VM:9093 | — |
| Pushgateway | http://IP_VM:9091 | — |
| Microservice | http://IP_VM:8000 | — |
| Métriques RED | http://IP_VM:8000/metrics | — |

## Structure du projet
```

telemetry-supervision/
├── docker-compose.yml          # Déclaration de tous les services
├── .env.example                # Template des variables d'environnement
├── prometheus/
│   ├── prometheus.yml          # Configuration scraping
│   └── rules/
│       └── alerting.rules.yml  # 12 règles d'alerting
├── alertmanager/
│   └── alertmanager.yml        # Routing des alertes
├── grafana/
│   ├── provisioning/           # Configuration automatique
│   │   ├── datasources/        # Connexion Prometheus
│   │   └── dashboards/         # Chargement automatique des dashboards
│   └── dashboards/             # Fichiers JSON des dashboards
├── telegraf/
│   └── telegraf.conf           # Bridge MQTT → Prometheus
├── mosquitto/
│   └── config/
│       └── mosquitto.conf      # Configuration broker MQTT
├── microservice/
│   ├── main.py                 # Application FastAPI + métriques RED
    ├── requirements.txt
    └── Dockerfile
└── simulateur-iot/
    ├── simulator.py            # Simulation de 4 capteurs IoT
    ├── requirements.txt
    └── Dockerfile

```
## Règles d'alerting

12 règles réparties sur 3 domaines :

**Infrastructure (5 règles)**
- `HighCPUUsage` — CPU > 85% pendant 2 minutes
- `HighMemoryUsage` — RAM > 85% pendant 2 minutes
- `DiskSpaceLow` — Disque > 80% pendant 5 minutes
- `HostDown` — Machine hôte injoignable
- `ContainerDown` — Conteneur Docker arrêté

**IoT (4 règles)**
- `SensorHighTemperature` — Température > 30°C
- `SensorLowBattery` — Batterie < 20%
- `SensorHighVibration` — Vibration > 1.5g
- `SensorDown` — Aucune donnée reçue depuis 2 minutes

**Applicatif (3 règles)**
- `HighErrorRate` — Taux d'erreur > 0.1/s pendant 2 minutes
- `HighLatency` — Latence p95 > 2 secondes
- `MicroserviceDown` — Microservice injoignable

## Métriques RED du microservice

| Métrique | Type | Description |
|----------|------|-------------|
| `http_requests_total` | Counter | Nombre total de requêtes (Rate) |
| `http_errors_total` | Counter | Nombre total d'erreurs (Errors) |
| `http_request_duration_seconds` | Histogram | Temps de réponse (Duration) |

## Flux de données IoT

Capteur publie → sensors/<device_id>/telemetry
Mosquitto distribue le message à Telegraf
Telegraf extrait température, pression, vibration, batterie
Telegraf expose les métriques sur :9273
Prometheus scrappe :9273 toutes les 15s
Alertmanager évalue les seuils
Grafana affiche les dashboards

## Auteur

Rayan Remila - Mohamed-Ali Zebli
Étudiant Master 1 — Informatique / Systèmes embarqués  
Année universitaire 2025-2026
