# Bilan de vérification

Contrôle du 16 septembre 2026 avec Claude Code **2.1.273** et le MCP public
`https://mcp.deepcopy.fr`. Ces observations décrivent ce contrôle, pas une garantie
de disponibilité future du service.

## Plugin

| Vérification | Résultat |
| --- | --- |
| Manifeste `.claude-plugin/plugin.json`, validation stricte | Réussite. |
| Marketplace `.claude-plugin/marketplace.json`, validation stricte | Réussite. |
| Répertoire `skills`, validation stricte | Réussite. |
| Inventaire avec `claude --plugin-dir . plugin details deepcopy` | Version 0.1.0, cinq skills, un MCP `momentum`. |
| Ajout de la marketplace locale et installation de `deepcopy@deepcopy-plugins` | Réussite dans une configuration Claude temporaire. |
| Inventaire après installation | Plugin activé, cinq skills et configuration HTTP attendue. |
| `claude mcp list` après installation | `plugin:deepcopy:momentum: https://mcp.deepcopy.fr (HTTP) - ✔ Connected`. |
| Tests Python du diagnostic | 7 tests réussis : JSON, SSE, corrélation des réponses, erreurs MCP et extraction des résultats. |

L'installation de test utilisait `CLAUDE_CONFIG_DIR` dans un dossier temporaire
et un répertoire de travail vide, sans installation dans la configuration
personnelle de l'utilisateur. Les contrôles réseau ont été effectués avec
l'accès réseau autorisé ; le bac à sable seul bloquait la résolution DNS.

## Service MCP

| Appel | Résultat observé |
| --- | --- |
| `initialize` | Réussite, serveur `Momentum Public`, compatibilité `2025-03-26`. |
| `tools/list` | Sept outils et leurs schémas récupérés. |
| `list_analyses`, limite 1 | Une analyse retournée. |
| `latest_analyses` | 45 analyses retournées. |
| `get_recommendations`, limite 1 | Une recommandation retournée. |
| `get_analysis`, UUID issu de `latest_analyses` | Détail ORCL retourné, identifiant concordant, `analysis_date: 2026-08-02`. |
| `latest_market_scan` | Échec applicatif : `isError: true`, `Momentum public API request failed.`, malgré HTTP 200. |
| `suggest_ticker` | Schéma vérifié ; aucune suggestion soumise pendant les tests. |
| `get_suggestion_status` | Schéma vérifié ; aucun appel avec un identifiant réel de suggestion. |

Le diagnostic `python3 scripts/check_mcp.py` sort donc avec le **code 1** lors de
ce contrôle : il détecte correctement l'échec du scan, puis vérifie quand même
le détail d'une analyse. Les validations locales du plugin et ses tests sont
réussis ; la disponibilité du scan dépend du service distant.

Les réponses d'analyses contiennent des dates historiques. Les skills imposent
leur restitution et ne présentent pas ces observations comme des cours du jour.

## Limites de la preuve

L'installation, l'inventaire des skills, la connexion du client natif et les
lectures MCP ci-dessus ont été vérifiés. Aucun test de réponse générée par le
modèle Claude, de création/modération d'une suggestion ou de publication du dépôt
n'a été effectué. Le plugin n'intègre aucune capacité administrative ou de
passage d'ordres.

Pour refaire les contrôles, utiliser les commandes de la section
[Développement et vérification](../README.md#développement-et-vérification).
