# Prometheus

## Rôle
Prometheus est le coeur du système de supervision. Il collecte (scrappe) les métriques
de toutes les sources toutes les 15 secondes et les stocke dans sa base de données
de séries temporelles (TSDB) pendant 15 jours.

## Fichiers

### prometheus.yml
Fichier de configuration principal de Prometheus.

| Section | Rôle |
|---------|------|
| `global` | Définit les intervalles de scraping et d'évaluation des règles |
| `alerting` | Indique à Prometheus où envoyer les alertes (Alertmanager) |
| `rule_files` | Charge les fichiers de règles d'alerting |
| `scrape_configs` | Liste toutes les cibles que Prometheus va interroger |

**Cibles scrappées** :
- `prometheus` — Prometheus se surveille lui-même
- `node-exporter` — métriques système Linux (port 9100)
- `cadvisor` — métriques conteneurs Docker (port 8080)
- `telegraf-iot` — métriques capteurs IoT (port 9273)
- `microservice` — métriques RED FastAPI (port 8000)
- `pushgateway` — métriques jobs éphémères (port 9091)

### rules/alerting.rules.yml
Contient les 12 règles d'alerting réparties en 3 groupes :

| Groupe | Règles | Domaine |
|--------|--------|---------|
| `infra` | 5 règles | CPU, RAM, disque, hôte, conteneurs |
| `iot` | 4 règles | température, batterie, vibration, capteur down |
| `app` | 3 règles | taux erreur, latence, microservice down |

## Interface web
Accessible sur `http://IP_VM:9090`

| Section | Utilité |
|---------|---------|
| Status → Targets | Vérifie que toutes les cibles sont UP |
| Alerts | Vérifie que les règles d'alerting sont chargées |
| Graph | Exécute des requêtes PromQL manuellement |
