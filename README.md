# Multi Service Updater

Permet d'ajouter plusieurs entités `update` dans Home Assistant pour gérer la mise à jour de services externes via une requête API sécurisée.

## Fonctionnalités

- Suivi de la version actuelle (via un sensor)
- Suivi de la dernière version disponible (via un autre sensor)
- Déclenchement de la mise à jour via un appel API sécurisé
- Ajout facile via l'interface graphique

## Installation

### Depuis HACS

1. Dans HACS > Intégrations, cliquez sur les trois points > Dépôt personnalisé.
2. Ajoutez `https://github.com/Rem7474/multi_service_updater` avec type `Intégration`.
3. Recherchez ensuite `Multi Service Updater` dans HACS et installez-la.

### Manuellement

1. Téléchargez ce dépôt.
2. Copiez le dossier `custom_components/multi_service_updater` dans `config/custom_components/`.
3. Redémarrez Home Assistant.

## Configuration

1. Allez dans `Paramètres > Appareils et services > Ajouter une intégration`.
2. Recherchez **Multi Service Updater**.
3. Renseignez :
   - Nom du service (`immich`, `vaultwarden`, etc.)
   - ID de l'entité sensor de la version actuelle (ex : `sensor.immich_current_version`)
   - ID de l'entité sensor de la dernière version (ex : `sensor.immich_latest_version`)
   - URL d'appel de mise à jour (ex : `https://update.remcorp.fr/immich/update`)
   - Token API (ex : `secret`)

## Exemple de sensor pour Immich

```yaml
sensor:
  - platform: rest
    name: "Immich Current Version"
    resource: "https://immich.remcorp.fr/api/server/version"
    method: GET
    headers:
      Accept: "application/json"
    value_template: >
      v{{ value_json.major }}.{{ value_json.minor }}.{{ value_json.patch }}
    scan_interval: 300
