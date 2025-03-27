# Multi-Service Updater

![hass-custom](https://img.shields.io/badge/Home%20Assistant-Custom%20Component-blue)
![version](https://img.shields.io/badge/version-1.1.0-blue)

Une intégration personnalisée Home Assistant pour gérer la mise à jour de plusieurs services auto-hébergés (comme Immich, Vaultwarden, etc.) en utilisant le système natif `update` de Home Assistant.

## Fonctionnalités

- Crée une entité `update` pour chaque service.
- Utilise les capteurs existants (`sensor`) pour déterminer la version actuelle et la dernière version disponible.
- Lance les mises à jour via une requête API sécurisée.
- Supporte les tokens d’authentification pour l’API de mise à jour.
- Interface graphique intégrée pour ajouter plusieurs services.

## Installation

1. Copiez le dossier `multi_service_updater` dans `config/custom_components/` de Home Assistant.
2. Redémarrez Home Assistant.
3. Ajoutez un service via `Paramètres > Intégrations > Ajouter une intégration > Multi-Service Updater`.
4. Renseignez les champs :
   - **Nom du service** (ex: `Immich`)
   - **Capteur version actuelle** (ex: `sensor.immich_current_version`)
   - **Capteur dernière version** (ex: `sensor.immich_latest_version`)
   - **URL de mise à jour** (ex: `https://update.remcorp.fr/immich/update`)
   - **Token API** *(optionnel)*

## Exemple d'appel API attendu

```bash
curl -X POST https://update.remcorp.fr/immich/update -H "Authorization: Bearer secret"
```

## Mise à jour de l’intégration

Téléchargez et exécutez ce script pour mettre à jour automatiquement :
```bash
bash <(curl -s https://raw.githubusercontent.com/Rem7474/multi_service_updater/main/install.sh)
```

## Auteur

Développé par **Rem7474**  
🔗 [github.com/Rem7474](https://github.com/Rem7474)