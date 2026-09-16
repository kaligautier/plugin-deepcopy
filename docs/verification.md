# Bilan de vérification

Contrôle du 16 septembre 2026 de la version **0.2.0**, avec Claude Code **2.1.273**
et le MCP public `https://mcp.deepcopy.fr`. Ces observations décrivent ce contrôle,
pas une garantie de disponibilité future du service.

## Plugin

| Vérification | Résultat |
| --- | --- |
| Manifeste `.claude-plugin/plugin.json`, validation stricte | Réussite. |
| Marketplace `.claude-plugin/marketplace.json`, validation stricte | Réussite. |
| Répertoire `skills`, validation stricte | Réussite. |
| Inventaire avec `claude --plugin-dir . plugin details deepcopy` | Version 0.2.0, quatre skills, un MCP `momentum`. |
| Ajout de la marketplace locale et installation de `deepcopy@deepcopy-plugins` | Réussite dans une configuration Claude temporaire. |
| Inventaire après installation | Version 0.2.0 activée, quatre skills : `analysis`, `recommendations`, `suggest`, `suggestion-status`. |
| Tests Python du diagnostic | 10 tests réussis : JSON/SSE, erreurs MCP, extraction des résultats et exécution limitée aux outils Momentum pris en charge. |

L'installation de test utilisait `CLAUDE_CONFIG_DIR` dans un nouveau dossier
temporaire et un répertoire de travail vide. Les contrôles réseau ont été
effectués avec l'accès réseau autorisé.

Les trois nouveaux tests prouvent que le diagnostic fonctionne avec les six
outils requis, ignore un outil de scan supplémentaire indisponible, et conserve
un code d'échec lorsqu'un outil Momentum pris en charge échoue. Ces tests
échouaient avant le retrait du scan.

## Service MCP

| Appel | Résultat observé |
| --- | --- |
| `initialize` | Réussite, serveur `Momentum Public`, compatibilité `2025-03-26`. |
| `tools/list` | Sept outils annoncés par le serveur ; les six utilisés par le plugin sont présents. |
| `list_analyses`, limite 1 | `isError: true`, `Momentum public API is unavailable.` |
| `latest_analyses` | `isError: true`, `Momentum public API is unavailable.` |
| `get_recommendations`, limite 1 | Une recommandation retournée. |
| `get_analysis` | Non testé en ligne : la lecture précédente n'a fourni aucun identifiant. Le chaînage est couvert par les tests locaux. |
| `suggest_ticker` | Schéma vérifié ; aucune suggestion soumise pendant les tests. |
| `get_suggestion_status` | Schéma vérifié ; aucun appel avec un identifiant réel de suggestion. |

Le diagnostic `python3 scripts/check_mcp.py` sort avec le **code 1** lors de ce
contrôle : les deux erreurs de consultation restent signalées. Aucun appel de
scan n'est effectué. Les validations locales du plugin et les tests sont réussis ;
ces erreurs réseau ne permettent pas de déclarer toutes les lectures disponibles.

La connexion MCP directe continue de restituer le catalogue du serveur distant.
Le retrait porte sur les skills, les instructions et le diagnostic du plugin ;
il ne masque pas les outils supplémentaires annoncés par ce serveur.

## Limites de la preuve

L'installation, l'inventaire des skills et les appels MCP ci-dessus ont été
vérifiés. Aucun test de réponse générée par le modèle Claude ou de création et
modération d'une suggestion n'a été effectué. Le plugin n'intègre aucune capacité
administrative ou de passage d'ordres.

Pour refaire les contrôles, utiliser les commandes de la section
[Développement et vérification](../README.md#développement-et-vérification).
