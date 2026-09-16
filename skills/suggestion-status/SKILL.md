---
name: suggestion-status
description: Vérifie le statut de modération d'une suggestion de ticker Momentum à partir de son suggestion_id, sans créer de nouvelle demande.
argument-hint: "<suggestion_id UUID>"
---

# Suivre une suggestion

Suggestion demandée : $ARGUMENTS

Lis et applique `${CLAUDE_PLUGIN_ROOT}/references/momentum.md`.

1. Utilise le `suggestion_id` UUID fourni ou celui explicitement associé à cette
   demande dans la conversation. Sans identifiant non ambigu, demande-le ; un
   ticker, un `job_id` ou un `analysis_id` ne le remplace pas.
2. Appelle `get_suggestion_status` une seule fois avec `suggestion_id`.
3. Rapporte les champs présents : symbole, statut, date de création, date de
   modération, motif de décision et identifiants associés.
4. Explique `pending` comme une attente de modération. Une approbation ne prouve
   pas qu'une analyse est terminée. Si une analyse est explicitement référencée,
   son contenu peut être vérifié avec `get_analysis` et son identifiant réel.

Une suggestion introuvable ou un service indisponible est une erreur de lecture,
pas un rejet par le modérateur. N'appelle pas `suggest_ticker` pour réparer cette
situation et ne mets pas en place de surveillance automatique.
