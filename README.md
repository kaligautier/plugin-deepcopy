# Deep Copy pour Claude Code

Les analyses Momentum et le scan de marché [Deep Copy](https://deepcopy.fr/#momentum-mcp)
dans Claude Code, avec cinq commandes et une connexion au MCP public
`https://mcp.deepcopy.fr`. Aucune clé API ni serveur local à installer.

## Démarrage rapide

Installe le plugin depuis sa marketplace GitHub :

```bash
claude plugin marketplace add kaligautier/plugin-deepcopy
claude plugin install deepcopy@deepcopy-plugins --scope user
```

Ouvre ensuite une nouvelle session Claude Code dans ton projet :

```text
/mcp
/deepcopy:analysis AAPL
/deepcopy:recommendations Buy,Overweight 5
/deepcopy:market-scan
```

`/mcp` permet de vérifier la connexion au serveur `momentum` du plugin `deepcopy`.
Claude Code gère les autorisations d'utilisation des outils. Le protocole est
négocié par son client MCP natif ; aucun en-tête de version n'est figé dans le plugin.

## Développement local

Pour charger directement une copie locale pendant une session :

```bash
claude --plugin-dir /chemin/vers/plugin-deepcopy
```

Tu peux aussi installer cette copie depuis la marketplace locale :

```bash
claude plugin marketplace add /chemin/vers/plugin-deepcopy
claude plugin install deepcopy@deepcopy-plugins --scope user
```

Ouvre ensuite une nouvelle session Claude Code dans ton projet. Le plugin sera
disponible sans `--plugin-dir`. Garde le dossier source accessible pour les
installations depuis une marketplace locale.

Le catalogue utilise `source: "./"` ; pour l'installation depuis GitHub, ajoute
le dépôt complet comme dans le démarrage rapide, pas l'URL brute de `marketplace.json`.

Pour retirer cette installation :

```bash
claude plugin uninstall deepcopy@deepcopy-plugins --scope user
```

## Commandes

| Commande | Usage |
| --- | --- |
| `/deepcopy:analysis AAPL` | Trouve la dernière analyse du ticker puis charge son détail avec son UUID réel. |
| `/deepcopy:analysis` | Liste les dernières analyses disponibles, avec leurs dates et identifiants. |
| `/deepcopy:analysis AAPL historique` | Consulte une page d'historique pour ce ticker. |
| `/deepcopy:recommendations Buy,Overweight 5` | Retourne jusqu'à cinq recommandations correspondant aux ratings. Sans argument : `Buy,Overweight`, limite 10. |
| `/deepcopy:market-scan` | Lit le dernier scan quotidien disponible et ses signaux par actif. |
| `/deepcopy:suggest ASML Suivre les prochains résultats` | Envoie explicitement une proposition de ticker à modérer. |
| `/deepcopy:suggestion-status <UUID>` | Consulte une suggestion avec le `suggestion_id` retourné par le service. |

`analysis` accepte aussi un UUID d'analyse. Remplace `<UUID>` par un identifiant
réel ; un symbole boursier ne remplace pas un `suggestion_id`.

Les quatre skills de lecture peuvent être sélectionnés par Claude lorsqu'une
demande correspond à leur description. `suggest` est réservé à l'invocation
manuelle grâce à `disable-model-invocation: true`. Consulter un ticker absent ne
crée pas de suggestion. Une suggestion `pending` attend une modération et ne
déclenche pas une analyse.

## Données et disponibilité

Les réponses citent leurs dates et identifiants. « Dernière disponible » ne
signifie pas « en temps réel » : les analyses peuvent dater de plusieurs mois.
Les recommandations et niveaux de prix sont ceux publiés par Momentum.

Une réponse HTTP 200 contenant `isError: true` reste une erreur. Le plugin la
signale au lieu de produire un résultat de remplacement. Au contrôle du
16 septembre 2026, les lectures d'analyses et de recommandations fonctionnaient,
mais `latest_market_scan` retournait `Momentum public API request failed.`.
Voir le [bilan de vérification](docs/verification.md) pour le périmètre testé.

Les sept outils et leurs paramètres sont détaillés dans
[la référence Momentum](references/momentum.md). Les schémas découverts sur le
serveur font autorité en cas d'évolution.

## Développement et vérification

Le plugin utilise uniquement du JSON et des skills Markdown. Python 3 est requis
uniquement pour le diagnostic et ses tests. Depuis le dossier du plugin :

```bash
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
claude plugin validate skills --strict
claude --plugin-dir . plugin details deepcopy
python3 -m unittest discover -s tests -v
python3 scripts/check_mcp.py
```

Le diagnostic initialise le MCP, découvre les outils, teste quatre lectures et
charge le détail d'un identifiant réellement retourné. Il affiche séparément les
outils non testés, ne soumet aucune suggestion et sort avec le code 1 si une
lecture testée échoue. Une liste vide valide est distinguée d'une erreur.
Ce script teste la compatibilité MCP `2025-03-26` du serveur ; la connexion
utilisée par Claude Code garde sa propre négociation de protocole.

Pendant le développement, recharge les modifications avec `/reload-plugins`
dans une session démarrée avec `--plugin-dir`.

```text
.claude-plugin/    Manifestes du plugin et de sa marketplace
.mcp.json         Connexion HTTP au MCP public
skills/           Cinq commandes Claude Code
references/       Paramètres et règles de restitution
scripts/          Diagnostic réseau à lancer explicitement
tests/            Tests du décodage JSON/SSE et des erreurs MCP
docs/             Bilan de vérification
SPEC.md           Périmètre et critères d'acceptation
```

## Références

- [Présentation du MCP Deep Copy](https://deepcopy.fr/#momentum-mcp)
- [Documentation MCP Deep Copy](https://deepcopy.fr/docs#mcp-tools)
- [Créer un plugin Claude Code](https://code.claude.com/docs/en/plugins)
- [Référence des plugins et manifestes](https://code.claude.com/docs/en/plugins-reference)
- [Connexion MCP dans Claude Code](https://code.claude.com/docs/en/mcp)
- [Créer et distribuer une marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
- [Tutoriel DataCamp fourni pour ce projet](https://www.datacamp.com/fr/tutorial/how-to-build-claude-code-plugins)
