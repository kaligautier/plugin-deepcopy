#!/usr/bin/env python3
"""Diagnostic explicite du MCP public ; aucune suggestion n'est envoyée."""

import json
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


EXPECTED_TOOLS = {
    "list_analyses", "latest_analyses", "get_analysis", "get_recommendations",
    "suggest_ticker", "get_suggestion_status",
}


def decode_response(body, request_id):
    """Accepte une réponse JSON ou l'événement SSE correspondant à la requête."""
    try:
        messages = [json.loads(body)]
    except json.JSONDecodeError:
        messages = []
        for event in body.replace("\r\n", "\n").split("\n\n"):
            data = "\n".join(
                line[5:].lstrip() for line in event.splitlines()
                if line.startswith("data:")
            )
            if data:
                messages.append(json.loads(data))
    for message in messages:
        if isinstance(message, dict) and message.get("id") == request_id:
            if "error" in message:
                raise ValueError(f"JSON-RPC : {message['error']}")
            result = message.get("result")
            if not isinstance(result, dict):
                raise ValueError("Résultat MCP manquant ou invalide")
            if result.get("isError") is True:
                detail = " ".join(
                    block.get("text", "") for block in result.get("content", [])
                    if block.get("type") == "text"
                )
                raise ValueError(f"isError=true : {detail}")
            return result
    raise ValueError("Aucune réponse MCP avec l'identifiant attendu")


def tool_data(result):
    if "structuredContent" in result:
        data = result["structuredContent"]
        return data["result"] if isinstance(data, dict) and set(data) == {"result"} else data
    text = "\n".join(
        block["text"] for block in result.get("content", [])
        if block.get("type") == "text"
    )
    return json.loads(text)


class Client:
    def __init__(self, url):
        self.url = url
        self.request_id = 0
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }

    def send(self, method, params, notification=False):
        self.request_id += 1
        payload = {"jsonrpc": "2.0", "method": method, "params": params}
        if not notification:
            payload["id"] = self.request_id
        request = Request(self.url, data=json.dumps(payload).encode(), headers=self.headers)
        with urlopen(request, timeout=30) as response:
            session_id = response.headers.get("Mcp-Session-Id")
            if session_id:
                self.headers["Mcp-Session-Id"] = session_id
            body = response.read().decode("utf-8")
        return None if notification else decode_response(body, self.request_id)


def main():
    root = Path(__file__).resolve().parents[1]
    version = json.loads((root / ".claude-plugin/plugin.json").read_text())["version"]
    config = json.loads((root / ".mcp.json").read_text())["mcpServers"]["momentum"]
    if config != {"type": "http", "url": "https://mcp.deepcopy.fr"}:
        raise ValueError("Ce diagnostic est réservé au MCP public Deep Copy sans authentification")
    client = Client(config["url"])
    protocol = "2025-03-26"
    info = client.send("initialize", {
        "protocolVersion": protocol,
        "capabilities": {},
        "clientInfo": {"name": "deepcopy-plugin-check", "version": version},
    })
    if info.get("protocolVersion") != protocol:
        raise ValueError(f"Version non prise en charge par ce diagnostic : {info.get('protocolVersion')}")
    client.headers["MCP-Protocol-Version"] = protocol
    client.send("notifications/initialized", {}, notification=True)
    print(f"OK initialize : {info['serverInfo']['name']} ({protocol})", flush=True)

    available = {tool["name"] for tool in client.send("tools/list", {})["tools"]}
    missing = EXPECTED_TOOLS - available
    if missing:
        raise ValueError(f"Outils manquants : {', '.join(sorted(missing))}")
    print(
        f"OK tools/list : {len(available)} outils exposés, "
        f"les {len(EXPECTED_TOOLS)} utilisés par le plugin sont présents",
        flush=True,
    )

    failures = 0
    latest = []
    for name, arguments in (
        ("list_analyses", {"limit": 1, "offset": 0}),
        ("latest_analyses", {}),
        ("get_recommendations", {"limit": 1}),
    ):
        try:
            data = tool_data(client.send("tools/call", {"name": name, "arguments": arguments}))
            if not isinstance(data, list):
                raise ValueError("Liste d'analyses attendue")
            summary = f"{len(data)} résultat(s)"
            if name == "latest_analyses":
                latest = data
            print(f"OK {name} : {summary}", flush=True)
        except (URLError, OSError, ValueError) as error:
            failures += 1
            print(f"ÉCHEC {name} : {error}", flush=True)

    if latest:
        try:
            analysis_id = latest[0]["id"]
            detail = tool_data(client.send("tools/call", {
                "name": "get_analysis", "arguments": {"analysis_id": analysis_id},
            }))
            if not isinstance(detail, dict) or detail.get("id") != analysis_id:
                raise ValueError("Le détail ne correspond pas à l'analyse demandée")
            print(f"OK get_analysis : id={analysis_id}, analysis_date={detail.get('analysis_date')}", flush=True)
        except (URLError, OSError, ValueError, KeyError, TypeError) as error:
            failures += 1
            print(f"ÉCHEC get_analysis : {error}", flush=True)
    else:
        print("NON TESTÉ get_analysis : aucun identifiant d'analyse disponible", flush=True)
    print("NON TESTÉ suggest_ticker : créerait potentiellement une suggestion", flush=True)
    print("NON TESTÉ get_suggestion_status : aucun identifiant de suggestion fourni", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (URLError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"ÉCHEC diagnostic : {error}", file=sys.stderr)
        sys.exit(1)
