---
layout: default
title: Divers
parent: Production
nav_order: 3
---

# Obsolescence — applications Java legacy

**Révision : 21/11/2026** · Périmètre : JBoss 4, Java 5/6, RHEL 5/6/7.

## Tableau d'obsolescence

| Composant | Fin de maintenance / support | Situation en 2026 | Action production |
|---|---|---|---|
| **RHEL 5** | ELS terminé le **30/11/2020** | **Obsolète — critique** | Sortir de RHEL 5 en priorité ; isoler en attendant |
| **RHEL 6** | ELS classique terminé le **30/06/2024** ; offre **ELS Long-Life jusqu'au 31/12/2030**, sous contrat et périmètre limité | **Legacy sous conditions** | Vérifier l'abonnement Long-Life et les paquets réellement couverts ; planifier la sortie |
| **RHEL 7** | Maintenance standard terminée le **30/06/2024** ; ELS possible jusqu'au **31/05/2029** pour RHEL 7.9 éligible | **Legacy sous conditions** | Vérifier ELS et couverture ; migrer vers OS maintenu |
| **Java 5** | Correctifs publics Oracle terminés en **2009** (support historique terminé) | **Obsolète — critique** | Tester une JVM plus récente sans recompilation ; sinon confinement |
| **Java 6 (OpenJDK Red Hat)** | Support Red Hat terminé le **31/12/2016** | **Obsolète — critique** | Évaluer une distribution Java 6 encore corrigée sous contrat ; préparer la migration |
| **JBoss AS 4.x / EAP 4.x** | Versions anciennes hors support courant ; **AS communautaire ≠ EAP commercial** | **Obsolète — critique** | Inventorier la variante exacte, fermer les consoles/invokers, envisager une migration middleware |

> **Attention :** une extension de support de l'OS **ne remet pas Java 5/6 ni JBoss 4 sous support**. Une JVM Java 6 alternative n'assure pas non plus le support de l'application.

## Plan d'action sans changement de code

1. **Inventorier** : OS et minor release, JBoss AS/EAP exact, JVM réellement lancée, architecture 32/64 bits, JAR, JDBC, TLS, flux et dépendances natives.
2. **Confinement immédiat** : réseau dédié, ports strictement nécessaires, proxy/WAF en frontal, bastion, consoles JMX/Web et invokers non exposés, sauvegardes et supervision.
3. **POC iso-code** : tester la même application avec une JVM patchée compatible, puis avec un OS récent. Valider transactions, JDBC, TLS, JNI, batchs et performances ; prévoir rollback.
4. **Arbitrage** : faire confirmer par l'éditeur les combinaisons certifiées et formaliser le risque résiduel, le responsable et la date cible de sortie.

### Diagnostic rapide (lecture seule)

```bash
cat /etc/redhat-release
uname -m
ps -ef | grep '[j]ava'
readlink -f /proc/<PID>/exe
rpm -qa | grep -Ei 'java|jdk|jre|jboss'
```

## Références éditeurs

- [Red Hat — cycle de vie RHEL 5 / fin ELS](https://access.redhat.com/articles/2986371)
- [Red Hat — RHEL 6 ELS Long-Life, jusqu'à fin 2030](https://access.redhat.com/support/policy/updates/rhel-els-long-life)
- [Red Hat — RHEL 7 ELS, jusqu'à mai 2029](https://www.redhat.com/fr/technologies/linux-platforms/enterprise-linux/upgrade-rhel)
- [Red Hat — cycle de vie OpenJDK](https://access.redhat.com/articles/1299013)
- [Oracle — fin de vie Java 5](https://www.oracle.com/java/technologies/javase/j2se-1-5.html)
- [Red Hat — archives du cycle de vie JBoss](https://access.redhat.com/support/policy/updates/jboss_notes/eol)
