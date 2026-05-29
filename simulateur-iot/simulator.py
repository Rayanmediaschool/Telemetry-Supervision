import json
import time
import random
import logging
from datetime import datetime
import paho.mqtt.client as mqtt

# ── CONFIGURATION ─────────────────────────────────────────
MQTT_BROKER = "mosquitto"   # Nom du service Docker
MQTT_PORT = 1883             # Port standard MQTT
PUBLISH_INTERVAL = 5         # Publie toutes les 5 secondes

# ── LOGGING ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ── DÉFINITION DES CAPTEURS ───────────────────────────────
# Chaque capteur a un identifiant, une localisation
# et des plages de valeurs normales
SENSORS = [
    {
        "id": "sensor_001",
        "location": "salle_serveurs",
        "type": "environnement"
    },
    {
        "id": "sensor_002",
        "location": "atelier_production",
        "type": "machine"
    },
    {
        "id": "sensor_003",
        "location": "entrepot",
        "type": "environnement"
    },
    {
        "id": "sensor_004",
        "location": "bureau",
        "type": "environnement"
    },
]

def generate_telemetry(sensor):
    """
    Génère des valeurs aléatoires réalistes pour un capteur.
    Simule 4 types de mesures : température, pression, vibration, batterie.
    Introduit occasionnellement des valeurs hors-seuil pour tester les alertes.
    """

    # Valeurs normales avec légère variation aléatoire
    temperature = round(random.uniform(18.0, 25.0), 2)
    pression = round(random.uniform(1010.0, 1020.0), 2)
    vibration = round(random.uniform(0.1, 0.5), 3)
    batterie = round(random.uniform(60.0, 100.0), 1)

    # 10% de chance de générer une valeur anormale (pour tester les alertes)
    if random.random() < 0.1:
        anomalie = random.choice(["temperature", "batterie", "vibration"])
        if anomalie == "temperature":
            temperature = round(random.uniform(35.0, 45.0), 2)  # Surchauffe
            logger.warning(f"[{sensor['id']}] Température anormale : {temperature}°C")
        elif anomalie == "batterie":
            batterie = round(random.uniform(5.0, 15.0), 1)       # Batterie faible
            logger.warning(f"[{sensor['id']}] Batterie faible : {batterie}%")
        elif anomalie == "vibration":
            vibration = round(random.uniform(2.0, 5.0), 3)       # Vibration excessive
            logger.warning(f"[{sensor['id']}] Vibration excessive : {vibration}")

    return {
        "device_id": sensor["id"],
        "location": sensor["location"],
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": temperature,     # en °C
        "pression": pression,           # en hPa
        "vibration": vibration,         # en g (accélération)
        "batterie": batterie            # en %
    }

def on_connect(client, userdata, flags, reason_code, properties):
    """Callback appelé quand le simulateur se connecte à Mosquitto"""
    if reason_code == 0:
        logger.info("Connecté au broker MQTT Mosquitto")
    else:
        logger.error(f"Echec de connexion, code : {reason_code}")

def main():
    """
    Boucle principale du simulateur.
    Se connecte à Mosquitto et publie en continu
    les télémétries de chaque capteur.
    """

    # Création du client MQTT
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect

    # Tentatives de connexion avec retry
    while True:
        try:
            logger.info(f"Connexion à Mosquitto sur {MQTT_BROKER}:{MQTT_PORT}...")
            client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            break
        except Exception as e:
            logger.error(f"Impossible de se connecter : {e}. Retry dans 5s...")
            time.sleep(5)

    client.loop_start()  # Démarre la boucle réseau en arrière-plan

    logger.info(f"Simulateur démarré — {len(SENSORS)} capteurs actifs")

    while True:
        for sensor in SENSORS:
            # Génère les données du capteur
            telemetry = generate_telemetry(sensor)

            # Topic MQTT : sensors/<device_id>/telemetry
            topic = f"sensors/{sensor['id']}/telemetry"

            # Publie le message en JSON sur Mosquitto
            payload = json.dumps(telemetry)
            client.publish(topic, payload, qos=1)

            logger.info(f"Publié sur {topic} : {payload}")

        # Attend avant la prochaine publication
        time.sleep(PUBLISH_INTERVAL)

if __name__ == "__main__":
    main()
