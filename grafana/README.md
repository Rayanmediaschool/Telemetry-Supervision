# Grafana

## Rôle
Grafana est l'interface de visualisation. Il se connecte à Prometheus
et affiche les métriques sous forme de dashboards interactifs.
Tout est provisionné automatiquement au démarrage — aucune action manuelle requise.

## Structure
```
grafana/
├── provisioning/
│   ├── datasources/
│   │   └── prometheus.yml    # Connexion automatique à Prometheus
│   └── dashboards/
│       └── dashboards.yml    # Chargement automatique des fichiers JSON
└── dashboards/
├── infrastructure.json   # Dashboard métriques Linux et Docker
├── iot.json              # Dashboard capteurs IoT
├── applicatif.json       # Dashboard métriques RED microservice
└── synthese.json         # Dashboard de synthèse multi-domaines
```

## Fichiers

### provisioning/datasources/prometheus.yml
Configure automatiquement la connexion entre Grafana et Prometheus.
Sans ce fichier, il faudrait configurer la datasource manuellement dans l'interface.

| Paramètre | Valeur | Rôle |
|-----------|--------|------|
| `url` | http://prometheus:9090 | Adresse de Prometheus sur le réseau Docker |
| `isDefault` | true | Datasource utilisée par défaut |
| `access` | proxy | Grafana fait les requêtes côté serveur |

### provisioning/dashboards/dashboards.yml
Indique à Grafana où trouver les fichiers JSON des dashboards.
Tout fichier JSON déposé dans `grafana/dashboards/` est automatiquement importé.

### dashboards/*.json
Les dashboards sont des fichiers JSON versionnés dans Git.
Ils sont chargés automatiquement au démarrage de Grafana.

| Fichier | Contenu |
|---------|---------|
| `infrastructure.json` | CPU, RAM, disque, conteneurs actifs |
| `iot.json` | Température, pression, vibration, batterie par capteur |
| `applicatif.json` | Rate, Errors, Duration du microservice FastAPI |
| `synthese.json` | Vue unifiée des 3 domaines |

## Interface web
Accessible sur `http://IP_VM:3000`
Identifiants : définis dans le fichier `.env` à la racine du projet
