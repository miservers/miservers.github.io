---
layout: default
title: CVE
parent: Security
nav_order: 4
---

- End-of-life: installer un logiciel en fin de vie exige à l'equipe d3 production de gerer eux memes les problematiques de securité. 
- OpenJDK 11: EOL octobre 2024
- Redis : version à installer 6.2.12
  * Cette versionbest touché par la CVE-2025-49844: criticité 10(HIGH). Elle permet d'executer un code malveillant  distance, c'est pour ça elle a été denommé RediShell. Cela vaut dire long sur la dangerousité de cette faille.
  * Toutes les version < 6.2.20 sont touchées par cette faille.
  * je ne trouve pas la 6.2.20 à telecharger sur le site oficielle de Redis. Donc on serait obligé d'installer une version superieur.
  * 6.2 a une EOL de Fev2025. c-a-d plus de support de la communauté, l'equipe de production doit gérer elle meme les choses si une faille de secu.
  * Sans demande explicite de la hierarchie, je ne pourai installer cette version
  * Comptabilité avec Redhat: seulement les version >= 7.4 sont compatibles avec RHEL 9. La compatibilité dans le cas de Redis est plus importante que Opensearch, puisque ce dernier est portable sur Java, alors que Redis est du code natif. 
  * FlowerDocs devrait permettre un Redis >= 7.4, la 7.2 arrive bientot en fin de vie(fev 2026) et la 6.4 l'est deja.
  
- Opensearch: 1.3.19
  * meme cas de figure, version obsolete . la version la plus recente est 3.3 
  * EOL mai 2025
  * OpenJDK 11: EOL octobre 2024
