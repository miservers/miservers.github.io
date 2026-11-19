---
layout: default
title: Alert Rules
parent: AppDynamics
grand_parent: DevOps
nav_order: 3
---

# AppDynamics — Alertes de production

**Controller on-premises 23.x.** Seuils indicatifs : calibrer sur trafic, baseline et SLO. Vérifier chaque métrique dans le **Metric Browser**.

## 1. Principes à retenir

| Périmètre | Méthode reconnue | Réflexe |
|:--|:--|:--|
| Services / Business Transactions | **RED — Tom Wilkie** : Rate, Errors, Duration | L'utilisateur termine-t-il sa transaction ? |
| Service (vue globale) | **Google SRE** : latence, trafic, erreurs, saturation | L'incident affecte-t-il le SLO ? |
| JVM / serveur | **USE — Brendan Gregg** : Utilization, Saturation, Errors | Quelle ressource limite le service ? |

**P1** = astreinte (impact utilisateur) ; **P2** = investigation ; **P3** = diagnostic. *Critical* AppDynamics n'implique pas automatiquement P1.

**Nommage proposé (non officiel)** : `PROD_<DOMAINE>_<CIBLE>_<SYMPTOME>` ; ex. `PROD_BT_LOGIN_LATENCE_ELEVEE`. Les anciens noms restent indiqués entre parenthèses.

## 2. Business Transactions (impact métier — RED)

| Health Rule conseillée (ancien nom) | Condition initiale / vérification | Priorité |
|:--|:--|:--:|
| `PROD_BT_ERREURS_ELEVEES` (`BT_Errors`) | Warning **>2 %** ; Critical **>5 % ET >10 erreurs/min** sur 5/10 min. Vérifier taux **et** volume. | P1 si impact |
| `PROD_BT_LATENCE_ELEVEE` (`BT_Slow`, `BT_TempsRéponse_Lent`) | Temps **moyen** > baseline +3σ et ≥30 appels/min sur 5/10 min ; alternative >2 s selon SLO. | P2 / P1 |
| `PROD_BT_P95_TROP_LENT` (`BT_TempsRéponse_TrèsLent`) | P95 >4 s **uniquement si le Controller expose cette métrique**. | P2 |
| `PROD_BT_TRAFIC_EN_BAISSE` (`BT_Trafic_Chute_Soudaine`) | Chute anormale du nombre d'appels ; exclure horaires creux et saisonnalité. | P2 |
| `PROD_BT_TAUX_LENTEUR_ELEVE` (`BT_Taux_Lenteur_Augmenté`) | Transactions lentes >10 % du total, avec volume minimal. | P2 |

**Login :** temps moyen de référence 1 100 ms ; +25 % = **1 375 ms**. Persistance `5/5 min` = cinq points. Baseline ≠ P95 ; adapter le critère de trafic.

## 3. Application (disponibilité et erreurs)

| Health Rule conseillée (ancien nom) | Condition initiale / vérification | Priorité |
|:--|:--|:--:|
| `PROD_APP_ENDPOINT_INDISPONIBLE` (`App_ServiceIndisponible_Endpoint`) | Échec de `/health` ou `/actuator/health` ; **sonde HTTP active requise** si endpoint non instrumenté. | P1 si service indisponible |
| `PROD_APP_ERREURS_HTTP_5XX` (`Erreur_HTTP_5xx_Elevée`) | HTTP 5xx >2 %, **si les codes sont réellement collectés** ; volume minimal. | P1 / P2 |
| `PROD_APP_EXCEPTIONS_NON_GEREES` (`Erreur_JAVA_Exception_Non_Gérée`) | Hausse des exceptions non gérées ; filtrer les classes utiles. | P2 |
| `PROD_APP_NOEUD_NON_REMONTANT` (`App_JVM_HS`) | Agent / nœud absent ou redémarré ; confirmer avec disponibilité applicative. **Agent absent ≠ JVM arrêtée.** | P2 |
| `PROD_APP_AUCUNE_REQUETE` (`App_Inactive_AucuneRequête`) | Zéro appel sur une BT habituellement active pendant X min ; exclure les heures creuses. | P2 |

**Diagnostic :** *Tiers & Nodes*, *Events*, snapshots. Exception Java ≠ HTTP 5xx ≠ erreur de BT.

## 4. JVM (saturation, GC, threads)

| Health Rule conseillée (ancien nom) | Condition initiale / vérification | Priorité |
|:--|:--|:--:|
| `PROD_JVM_HEAP_SATURE` (`JVM_Heap_Memory_Saturé`) | Heap >85 % ; **observer surtout l'occupation après GC et sa tendance**. | P2 |
| `PROD_JVM_FULL_GC_FREQUENT` (`JVM_FullGC_Frequence_Elevée`) | >5 Full GC/min **à titre d'exemple** ; examiner pauses, collecteur et latence utilisateur. | P2 |
| `PROD_JVM_CPU_ELEVE` (`JVM_CPU_Taux_Elevé`) | CPU processus JVM >90 % durablement ; distinguer CPU processus et CPU machine. | P2 |
| `PROD_JVM_THREADS_BLOQUES` (`JVM_Threads_Bloqués`) | Threads bloqués > seuil applicatif ; vérifier *Thread Contention* et thread dumps. | P2 |

**GC :** heap élevé ≠ fuite. Examiner heap **après GC** et pauses selon collecteur/JVM.

## 5. Dépendances (bases, API et messaging)

| Health Rule conseillée (ancien nom) | Condition initiale / vérification | Priorité |
|:--|:--|:--:|
| `PROD_DEP_DB_LATENCE_ELEVEE` (`DB_TempsRéponse_Lent`) | Appels DB >1 s ou >baseline ; cibler le backend. | P2 |
| `PROD_DEP_DB_ERREURS_ELEVEES` (`DB_Erreurs_Fréquentes`) | Erreurs DB >2 % ; identifier la base, le pool et les timeouts. | P2 |
| `PROD_DEP_API_LATENCE_ELEVEE` (`API_Tiers_Réponse_Lente`) | REST externe >2 s ; isoler l'URL / backend concerné. | P2 |
| `PROD_DEP_API_ERREURS_REPETEES` (`API_Tiers_Erreurs_Répétées`, `Erreur_API_Externe`) | >3 échecs/min sur un même service (exemple) ; confirmer la classification des erreurs. | P2 |
| `PROD_DEP_MESSAGING_LATENCE` (`Actuator_Latence_File_Message`) | Latence de traitement Kafka/RabbitMQ > seuil métier ; **custom metric requise** si non collectée. | P2 |

**Diagnostic :** *Backends / Exit Calls*, JDBC, timeouts. RabbitMQ : latence de traitement ≠ âge des messages en file.

## 6. Infrastructure (USE)

| Health Rule conseillée (ancien nom) | Condition initiale / vérification | Priorité |
|:--|:--|:--:|
| `PROD_INFRA_CPU_SATURE` (`CPU_Hot`, `INFRA_CPU_HIGH`) | Warning >75 % ; Critical >85 %, par exemple 5/5 min. Vérifier CPU **et** saturation. | P2 |
| `PROD_INFRA_MEMOIRE_SATUREE` (`Memory_Pressure`, `INFRA_USED_MEMORY_HIGH`) | Warning >75 % ; Critical >90 %. Corréler avec mémoire disponible / swap. | P2 |
| `PROD_INFRA_PROCESSUS_ABSENT` (`Linux_Process_Missing`) | Processus absent ; extension / process monitoring nécessaire. Chemin de métrique à vérifier. | P2 |
| `PROD_INFRA_MACHINE_AGENT_ABSENT` (`INFRA_MACHINE_AGENT_HS`) | Machine Agent non remontant pendant ~5 min ; **perte de supervision**, pas panne applicative prouvée. | P2 |

**Prérequis :** Machine Agent + **Server Visibility** si requis ; vérifier chemins/unités. Exemple à confirmer : `Hardware Resources/Process/<process-name>|Count`.

## 7. KPI métier (métriques personnalisées)

| Health Rule conseillée (ancien nom) | Condition initiale / vérification | Priorité |
|:--|:--|:--:|
| `PROD_KPI_UTILISATEURS_ACTIFS_BAS` (`Actuator_UtilisateursActifs_Baisse`) | Utilisateurs actifs < seuil adapté aux horaires. | P2 / P3 |
| `PROD_KPI_CONVERSION_EN_BAISSE` (`Actuator_TauxConversion_Baisse`) | Taux de conversion inférieur à la référence, à trafic comparable. | P2 / P3 |

**Actuator ≠ métrique AppDynamics** : prévoir l'intégration et vérifier son chemin.

## 8. Configurer une alerte dans AppDynamics 23.x

### Étape A — Health Rule

`Alert & Respond > Health Rules > +` → **Overview** (nom, *Enabled*, schedule, fenêtre) → **Affected Entities** (BT/tier/node) → **Critical / Warning Conditions** (métrique, seuil, persistance) → **Save**.

![Capture AppDynamics : création d'une Health Rule, écran 1](/docs/images/appdynamics/Appdynamics-HR-1.jpg)

![Capture AppDynamics : création d'une Health Rule, écran 2](/docs/images/appdynamics/Appdynamics-HR-2.jpg)

### Étape B — Action, puis Policy

`Alert & Respond > Actions` : réutiliser ou créer `Notif_Email_Incident_Critique`, `Notif_Slack_Warning_App` ou `Notif_PagerDuty_Downtime` selon les intégrations disponibles. Pour l'email, vérifier la configuration **SMTP** du Controller.

`Alert & Respond > Policies` : nom `POL_PROD_BT_CRITICAL` → sélectionner les Health Rules souhaitées → événement **Health Rule Violation Started - Critical** → lier l'action. Configurer *Warning* si nécessaire.

![Capture AppDynamics : configuration d'une Policy, écran 1](/docs/images/appdynamics/Appdynamics-POL-1.jpg)

![Capture AppDynamics : configuration d'une Policy, écran 2](/docs/images/appdynamics/Appdynamics-POL-2.jpg)

**Rappels :** `Continues` facultatif ; régler `Wait Time after Violation`.

### Exemple complet — Erreurs sur la BT Login

| Champ | Valeur à adapter |
|:--|:--|
| Nom | `PROD_BT_LOGIN_ERREURS_ELEVEES` |
| Type / scope | *Business Transaction Performance* / **Login** uniquement |
| Warning | Erreurs >2 % et trafic minimal pertinent |
| Critical | Erreurs >5 % **ET** >10 erreurs/min |
| Évaluation | 10 min, persistance **5 fois** |
| Policy | `POL_PROD_BT_CRITICAL` → *Started - Critical* → `Notif_Email_Incident_Critique` |
| Vérification | Graphes **Errors per Minute** / **Calls per Minute**, violation, email reçu |

**Vérifier** la métrique de taux d'erreurs ou créer une expression à partir des mesures disponibles. **Tester hors production**.

## 9. Vérification / dépannage (fiche réflexe)

| Symptôme | Contrôle prioritaire |
|:--|:--|
| **Unknown / aucune donnée** | Agent, Metric Browser, fenêtre, `Evaluate to true on no data`. Ne pas assimiler automatiquement un manque de données à une panne du service. |
| **Violation sans notification** | Policy activée, événement *Started*, scope, Action, destinataire, SMTP, suppressions. |
| **Trop de notifications** | Regrouper par impact, minimum de trafic, persistance, schedule, supprimer les `Continues` superflus. |
| **Règle jamais déclenchée** | Métrique exacte, unité, opérateur, scope, `ALL` / `ANY`, période, historique. |

![Capture AppDynamics : état des Health Rules](/docs/images/appdynamics_RulesStatus.png)

**Captures complémentaires :** [HR 3](/docs/images/appdynamics/Appdynamics-HR-3.jpg) · [HR 4](/docs/images/appdynamics/Appdynamics-HR-4.jpg) · [Policy 3](/docs/images/appdynamics/Appdynamics-POL-3.jpg) · [Policy 4](/docs/images/appdynamics/Appdynamics-POL-4.jpg) · [Metric Browser](/docs/images/appdynamics-metrics-browser.jpg)

**Chaque alerte :** application, scope, seuil, contact, runbook, action. Revoir les seuils après incident.

## Références

- [Google SRE — Monitoring Distributed Systems (Four Golden Signals)](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Google SRE Workbook — Monitoring et niveaux d'alerte](https://sre.google/workbook/monitoring/)
- [Tom Wilkie — The RED Method (Grafana Labs)](https://grafana.com/blog/the-red-method-how-to-instrument-your-services/)
- [Brendan Gregg — The USE Method](https://www.brendangregg.com/usemethod.html)
- [AppDynamics 23.x — Create a Health Rule](https://docs.appdynamics.com/appd/23.x/latest/en/appdynamics-essentials/alert-and-respond/configure-health-rules/create-a-health-rule)
- [AppDynamics On-Prem 23.x — Health Rule Conditions](https://docs.appdynamics.com/appd/onprem/23.x/23.11/en/appdynamics-essentials/alert-and-respond/health-rules/health-rule-conditions)
- [AppDynamics 23.x — Policies](https://docs.appdynamics.com/appd/23.x/latest/en/appdynamics-essentials/alert-and-respond/policies)
- [AppDynamics 23.x — Actions](https://docs.appdynamics.com/appd/23.x/latest/en/appdynamics-essentials/alert-and-respond/actions)
- [AppDynamics 23.x — Machine Agent / custom metrics](https://docs.appdynamics.com/appd/23.x/latest/en/infrastructure-visibility/machine-agent)
- [AppDynamics 23.x — Troubleshooting Alert & Respond](https://docs.appdynamics.com/appd/23.x/latest/en/appdynamics-essentials/alert-and-respond/troubleshoot-alert-and-respond-problems)
- [AppDynamics 23.x — API Health Rules](https://docs.appdynamics.com/appd/23.x/latest/en/extend-appdynamics/appdynamics-apis/alert-and-respond-api/health-rule-api)
