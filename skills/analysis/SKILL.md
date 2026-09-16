---
name: analysis
description: Consulte les analyses publiques Momentum de Deep Copy pour un ticker ou un UUID. Utilise ce skill pour résumer une analyse, examiner ses fondamentaux et signaux techniques, ou lire son historique.
argument-hint: "[ticker ou UUID] [historique]"
---

# Consulter une analyse Momentum

Demande : $ARGUMENTS

Lis et applique `${CLAUDE_PLUGIN_ROOT}/references/momentum.md`.

1. Sans argument ni ticker clairement fourni dans la demande, appelle
   `latest_analyses` avec `{}`. Présente au plus dix résultats avec ticker, date,
   rating et `id`, et précise si tu limites l'affichage.
2. Avec un UUID d'analyse, appelle `get_analysis` avec cet `analysis_id`.
3. Avec un ticker, appelle `latest_analyses` avec `ticker`, puis charge le détail
   via `get_analysis` en reprenant le champ `id` du résultat correspondant.
   Si le symbole ou la place boursière est ambigu, fais préciser le ticker.
4. Pour un historique, utilise `list_analyses` avec `ticker`, `limit: 10` et
   `offset: 0`. Ne suppose pas l'ordre chronologique de la page ; affiche les
   dates et utilise la pagination seulement si la demande le nécessite.
5. Si la lecture réussit sans résultat, indique qu'aucune analyse n'est disponible
   pour ce filtre. Mentionne `/deepcopy:suggest TICKER` comme action possible.
   Une erreur du service doit être rapportée comme une erreur de consultation.

Pour un détail, commence par le ticker, la date de l'analyse, son identifiant et
le rating Momentum. Résume ensuite les arguments fondamentaux, techniques,
actualités/sentiment et scénarios bull/bear présents dans la réponse. Termine par
les niveaux de prix, l'horizon et les risques documentés. Signale l'ancienneté des
données et les champs manquants. Si seul le résumé est accessible, annonce cette
limite plutôt que de compléter le détail de mémoire.
