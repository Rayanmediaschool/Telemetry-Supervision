# Simulateur IoT

## Rôle
Script Python qui simule 4 capteurs physiques.
Il génère des valeurs aléatoires réalistes et les publie
en MQTT sur Mosquitto toutes les 5 secondes.

## Fichiers

| Fichier | Rôle |
|---------|------|
| `simulator.py` | Code source du simulateur |
| `requirements.txt` | Dépendances Python (paho-mqtt) |
| `Dockerfile` | Instructions de construction de l'image Docker |

## Les 4 capteurs simulés

| ID | Localisation | Type |
|----|-------------|------|
| `sensor_001` | salle_serveurs | environnement |
| `sensor_002` | atelier_production | machine |
| `sensor_003` | entrepot | environnement |
| `sensor_004` | bureau | environnement |

## Métriques publiées

| Métrique | Unité | Plage normale | Seuil d'alerte |
|----------|-------|---------------|----------------|
| `temperature` | °C | 18 à 25 | > 30 |
| `pression` | hPa | 1010 à 1020 | — |
| `vibration` | g | 0.1 à 0.5 | > 1.5 |
| `batterie` | % | 60 à 100 | < 20 |

## Format des messages MQTT

Topic : `sensors/<device_id>/telemetry`

Payload JSON :

```json
{
  "device_id": "sensor_001",
  "location": "salle_serveurs",
  "timestamp": "2026-06-01T10:00:00",
  "temperature": 22.5,
  "pression": 1013.2,
  "vibration": 0.3,
  "batterie": 85.0
}
```

## Anomalies simulées
Le simulateur génère des valeurs hors-seuil 10% du temps
pour tester le déclenchement des alertes Prometheus :
- Température entre 35°C et 45°C (surchauffe)
- Batterie entre 5% et 15% (batterie critique)
- Vibration entre 2g et 5g (vibration excessive)

## Vérifier les logs

```bash
docker compose logs simulateur-iot -f
```
