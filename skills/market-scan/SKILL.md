---
name: market-scan
description: Consulte le dernier scan de marché quotidien Deep Copy, son régime et ses signaux par actif. Utilise ce skill pour obtenir le contexte de marché publié par le Market Scanner.
argument-hint: "[actif ou angle de lecture facultatif]"
---

# Lire le dernier scan de marché

Angle de lecture demandé : $ARGUMENTS

Lis et applique `${CLAUDE_PLUGIN_ROOT}/references/momentum.md`.

1. Appelle `latest_market_scan` avec `{}`. Les arguments de la commande servent
   à orienter la synthèse, pas à ajouter des paramètres à cet outil.
2. Vérifie que l'appel a réussi avant toute synthèse. En cas d'erreur, rapporte
   que le scan est indisponible et le message retourné. Ne déduis pas le régime
   du jour des anciennes analyses Momentum ni de connaissances générales.
3. Donne la date du scan et son identifiant s'il existe. Signale un scan ancien.
4. Présente le régime global, les facteurs explicatifs et les éventuels scores
   ou probabilités avec leurs unités, uniquement si le service les fournit.
5. Synthétise les signaux par actif : nom, direction, intensité, justification
   et risques selon les champs disponibles. Si un actif demandé est absent,
   indique-le sans lui attribuer un signal.

Attribue les résultats au Market Scanner Deep Copy. Sépare la lecture globale
du scan des conclusions spécifiques à un titre ; ne prétends pas avoir obtenu
une analyse Momentum complète à partir de ce seul outil.
