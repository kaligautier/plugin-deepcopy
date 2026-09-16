---
name: recommendations
description: Consulte les recommandations Momentum publiées par Deep Copy et filtre les analyses par rating Buy, Overweight, Hold, Underweight ou Sell.
argument-hint: "[ratings séparés par des virgules] [limite de 1 à 100]"
---

# Consulter les recommandations Momentum

Filtres demandés : $ARGUMENTS

Lis et applique `${CLAUDE_PLUGIN_ROOT}/references/momentum.md`.

1. Utilise `rating: "Buy,Overweight"` et `limit: 10` lorsque l'utilisateur ne
   précise pas de filtre. Reprends ses filtres lorsqu'ils sont valides ; si un
   rating est inconnu ou une limite hors de 1 à 100, demande une valeur valide.
2. Appelle `get_recommendations` avec `rating` et `limit`. Une demande ciblant un
   ticker se traite avec `latest_analyses` filtré par `ticker`.
3. Affiche un tableau des champs disponibles : ticker, date d'analyse, rating,
   prix d'entrée, objectif, stop, horizon et ratio risque/rendement. Conserve
   les valeurs et unités de la source et donne l'identifiant de chaque analyse.
4. Résume les arguments et risques présents. Charge un détail avec `get_analysis`
   seulement si la demande nécessite plus que les résumés.

Présente ces résultats comme les recommandations datées de Momentum. Une liste
vide indique l'absence de résultats pour le filtre, pas l'absence d'opportunités
sur le marché. Ne présente pas le classement du serveur comme une performance
mesurée et n'assimile pas ses niveaux de prix à des cours actuels.
