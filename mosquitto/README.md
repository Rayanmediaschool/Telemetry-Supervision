# Mosquitto

## Rôle
Mosquitto est le broker MQTT du projet. Il reçoit les messages
publiés par les capteurs IoT et les redistribue aux subscribers (Telegraf).
C'est le "facteur" du réseau IoT.

## Structure
```
mosquitto/
├── config/
│   └── mosquitto.conf    # Configuration du broker
├── data/                 # Persistance des messages (ignoré par Git)
└── log/                  # Logs du broker (ignoré par Git)
```
## Fichiers

### config/mosquitto.conf
Fichier de configuration principal de Mosquitto.

| Paramètre | Valeur | Rôle |
|-----------|--------|------|
| `listener` | 1883 | Port d'écoute standard MQTT |
| `allow_anonymous` | true | Autorise les connexions sans authentification |
| `persistence` | true | Sauvegarde les messages sur disque |
| `persistence_location` | /mosquitto/data/ | Dossier de persistance |
| `log_dest` | file | Écrit les logs dans un fichier |

## Protocol MQTT

MQTT fonctionne avec un système de topics et de messages :
- **Publisher** (simulateur-iot) → publie sur `sensors/<device_id>/telemetry`
- **Broker** (mosquitto) → reçoit et redistribue les messages
- **Subscriber** (telegraf) → souscrit à `sensors/#` et reçoit tous les messages

## Port
Mosquitto écoute sur le port `1883` (port standard MQTT).

## Sécurité
En développement `allow_anonymous true` est activé.
En production il faut :
- Passer `allow_anonymous` à `false`
- Créer des comptes avec `mosquitto_passwd`
- Activer TLS sur le port 8883
