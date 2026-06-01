# Alertmanager

## Rôle
Alertmanager reçoit les alertes déclenchées par Prometheus et les route vers
le bon canal de notification selon leur domaine (infra, IoT, applicatif).
Il gère aussi la déduplication pour éviter le spam d'alertes.

## Fichiers

### alertmanager.yml
Fichier de configuration principal d'Alertmanager.

| Section | Rôle |
|---------|------|
| `global` | Paramètres globaux (timeout de résolution) |
| `route` | Arbre de décision pour router les alertes |
| `receivers` | Définit où envoyer les alertes (webhook, Slack, email) |

**Logique de routage** :
```

Alerte reçue
↓
Label domain = infra ? → infra-receiver
Label domain = iot ?   → iot-receiver
Label domain = app ?   → app-receiver
Sinon                  → default
```

**Paramètres de déduplication** :
- `group_by` — regroupe les alertes par nom et domaine
- `group_wait` — attend 30s avant d'envoyer le premier groupe
- `group_interval` — délai entre deux notifications du même groupe
- `repeat_interval` — répète l'alerte toutes les heures si non résolue

## Interface web
Accessible sur `http://IP_VM:9093`

| Section | Utilité |
|---------|---------|
| Alerts | Liste les alertes actives |
| Silences | Permet de mettre en silence une alerte temporairement |
| Status | Affiche la configuration chargée |
