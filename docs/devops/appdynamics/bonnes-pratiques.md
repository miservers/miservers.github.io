---
layout: default
title: Bonnes Pratiques
parent:  AppDynamics
grand_parent: DevOps
nav_order: 2
---

### Identifier les Business Transaction
une BT est action metier top-niveau du point de vue de l'utilisateur. Exemples: Login, Ajouter au panier, Payer, Télacharger une Facture,etc.

Une BT peut être une suite d'actions, c-a-d un parcours utilisateur mesurable.

Appdynamics detecte automatiquement toutes les BT. Tu peux commencer par celles qui ont un trafic ou temps de reponse elevés.

### Definir les KPIs: Key Perfomance Indicators
Il faut definir les KPIs et ensuite les appliquer aux  Business Transactions.
1. **KPIs Communs**
   - Load: mesure le nombre tolal d'appels par minute.
   - Response Time: temps de reponse moyen(ou 95 Percentile), en ms.
   - Error Rate: inclut le nombre total et types d'erreurs par minute
   

   
