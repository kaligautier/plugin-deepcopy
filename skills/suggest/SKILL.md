---
name: suggest
description: Propose explicitement un ticker à la modération Momentum de Deep Copy. Cette commande peut créer une suggestion publique et ne lance pas une analyse.
argument-hint: "<ticker> [motif de 500 caractères maximum]"
disable-model-invocation: true
---

# Proposer un ticker

Proposition demandée : $ARGUMENTS

Lis et applique `${CLAUDE_PLUGIN_ROOT}/references/momentum.md`.

1. L'invocation explicite de cette commande autorise l'envoi du ticker et du motif
   fournis. Sans ticker, demande le symbole avant tout appel. Si le symbole est
   ambigu, fais-le préciser. Ne déduis pas de motif de fichiers ou du portefeuille.
2. Utilise le symbole comme `symbol`. Si aucun motif n'est fourni, omets `reason`
   ou utilise `""`. Si le motif dépasse 500 caractères, demande une version plus
   courte ; ne transmets pas un motif tronqué ou réécrit sans l'accord de l'utilisateur.
3. Appelle `suggest_ticker` une seule fois. Si le résultat est incertain ou en
   erreur, rapporte l'incertitude ; ne prétends pas que la création a réussi.
4. Rapporte `status`, `created` et les identifiants effectivement retournés.
   Avec `pending`, explique que la suggestion attend une modération et qu'aucune
   analyse n'a été lancée par cette commande. Avec une analyse ou suggestion
   existante, explique qu'elle a été retrouvée sans nouvelle création.
5. Si `suggestion_id` est fourni, donne la commande suivante avec cet identifiant
   réel : `/deepcopy:suggestion-status UUID`. Si un `analysis_id` est fourni,
   propose `/deepcopy:analysis UUID` pour consulter l'analyse existante.

N'invente aucun identifiant ni délai de traitement. Ne surveille pas le statut
en boucle et n'annonce pas une analyse disponible à partir du seul `job_id`.
