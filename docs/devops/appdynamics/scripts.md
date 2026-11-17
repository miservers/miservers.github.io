---
layout: default
title: Scripts
parent:  AppDynamics
grand_parent: DevOps
nav_order: 30
---


### Export config Appdynamics
~~~sh

# =========================================
# Ce script exporte Applications, Health Rules, Policies, Actions et Dashboards
# dans un dossier horodaté.
# Il utilise un token OAuth généré depuis un API Client (pour les environnements SSO)
# =========================================

# -----------------------------
# CONFIGURATION
# -----------------------------
CONTROLLER="https://controller-host/controller"
CLIENT_ID="VOTRE_CLIENT_ID"         # API Client ID créé dans AppDynamics
CLIENT_SECRET="CHANGE_ME" # API Client Secret
# NOTE : Pour obtenir CLIENT_ID et CLIENT_SECRET :
# 1. Connectez-vous à AppDynamics via SSO avec un compte admin.
# 2. Allez dans Settings → Users & Roles → API Clients → Create API Client
# 3. Donnez un nom, sélectionnez les rôles nécessaires, puis créez le client.
# 4. Sauvegardez le Client Secret affiché (il ne sera plus visible après)

EXPORT_DIR="appd_export_$(date +%Y%m%d_%H%M%S)"
mkdir -p $EXPORT_DIR

# -----------------------------
#  Générer le token OAuth
# -----------------------------
echo "Génération du token OAuth via API Client..."
TOKEN=$(curl -s -X POST "$CONTROLLER/controller/api/oauth/access_token" \
  -d "client_id=$CLIENT_ID&client_secret=CHANGE_ME" \
  | jq -r '.access_token')

if [ -z "$TOKEN" ]; then
  echo "Erreur : impossible de générer le token OAuth. Vérifie CLIENT_ID et CLIENT_SECRET."
  exit 1
fi

echo "Token généré avec succès."

# -----------------------------
#  Exporter toutes les applications
# -----------------------------
echo "Export des applications..."
curl -s -H "Authorization: Bearer $TOKEN" \
  $CONTROLLER/rest/applications \
  > $EXPORT_DIR/applications.xml

APP_IDS=$(grep -oPm1 "(?<=<id>)[^<]+" $EXPORT_DIR/applications.xml)

# -----------------------------
# Export des configurations par application
# -----------------------------
for APP_ID in $APP_IDS
do
  APP_DIR="$EXPORT_DIR/application_$APP_ID"
  mkdir -p $APP_DIR

  echo "Export application ID: $APP_ID"

  # Health Rules
  curl -s -H "Authorization: Bearer $TOKEN" \
    $CONTROLLER/healthrules/$APP_ID \
    > $APP_DIR/healthrules.xml

  # Policies
  curl -s -H "Authorization: Bearer $TOKEN" \
    $CONTROLLER/policies/$APP_ID \
    > $APP_DIR/policies.xml

  # Actions
  curl -s -H "Authorization: Bearer $TOKEN" \
    $CONTROLLER/actions/$APP_ID \
    > $APP_DIR/actions.xml

  # Dashboards
  curl -s -H "Authorization: Bearer $TOKEN" \
    $CONTROLLER/dashboards/$APP_ID \
    > $APP_DIR/dashboards.xml
done

# -----------------------------
# Export des règles globales
# -----------------------------
echo "Export des règles et policies globales..."

curl -s -H "Authorization: Bearer $TOKEN" \
  $CONTROLLER/healthrules \
  > $EXPORT_DIR/global_healthrules.xml

curl -s -H "Authorization: Bearer $TOKEN" \
  $CONTROLLER/policies \
  > $EXPORT_DIR/global_policies.xml

curl -s -H "Authorization: Bearer $TOKEN" \
  $CONTROLLER/actions \
  > $EXPORT_DIR/global_actions.xml

echo "Export terminé dans le dossier : $EXPORT_DIR"
~~~