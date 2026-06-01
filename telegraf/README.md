# Telegraf

## Rôle
Telegraf fait le pont entre le monde MQTT et Prometheus.
Il souscrit aux topics MQTT de Mosquitto, lit les messages JSON
des capteurs et les convertit au format Prometheus.

## Flux de données
```
Mosquitto (MQTT) → Telegraf → format Prometheus → Prometheus (scraping)
```

## Fichiers

### telegraf.conf
Fichier de configuration principal de Telegraf.

| Section | Rôle |
|---------|------|
| `[agent]` | Paramètres globaux (intervalle de collecte, nom) |
| `[[inputs.mqtt_consumer]]` | Souscrit aux topics MQTT de Mosquitto |
| `[[outputs.prometheus_client]]` | Expose les métriques sur le port 9273 |

**Topics MQTT écoutés** :
- `sensors/#` — tous les topics sous sensors/ (wildcard #)

**Métriques extraites des messages JSON** :
- `mqtt_consumer_temperature` — température en °C
- `mqtt_consumer_pression` — pression en hPa
- `mqtt_consumer_vibration` — vibration en g
- `mqtt_consumer_batterie` — niveau batterie en %

**Tags extraits** :
- `device_id` — identifiant du capteur
- `location` — localisation du capteur

## Port
Telegraf expose les métriques sur le port `9273`.
Prometheus vient scraper ce port toutes les 15 secondes.
