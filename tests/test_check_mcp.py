import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from scripts import check_mcp
from scripts.check_mcp import decode_response, tool_data


class ResponseTests(unittest.TestCase):
    def test_json_and_sse_return_the_same_result(self):
        payload = {"jsonrpc": "2.0", "id": 7, "result": {"content": [], "isError": False}}
        encoded = json.dumps(payload)
        bodies = [encoded, f"event: message\r\ndata: {encoded}\r\n\r\n"]
        for body in bodies:
            with self.subTest(body=body):
                self.assertEqual(decode_response(body, 7), payload["result"])

    def test_sse_ignores_notifications_and_joins_data_lines(self):
        body = (
            ': keepalive\n\nevent: message\ndata: {"method":"notifications/message"}\n\n'
            'event: message\ndata: {"id":7,\ndata: "result":{"content":[]}}\n\n'
        )
        self.assertEqual(decode_response(body, 7), {"content": []})

    def test_successful_http_body_can_contain_a_tool_failure(self):
        body = json.dumps({"id": 7, "result": {
            "isError": True,
            "content": [{"type": "text", "text": "Momentum public API request failed."}],
        }})
        with self.assertRaisesRegex(ValueError, "isError=true.*request failed"):
            decode_response(body, 7)

    def test_json_rpc_failure_is_not_a_success(self):
        with self.assertRaisesRegex(ValueError, "JSON-RPC"):
            decode_response('{"id":7,"error":{"code":-32602,"message":"Invalid params"}}', 7)

    def test_missing_result_and_wrong_request_id_are_rejected(self):
        for body in ('{"id":7}', '{"id":8,"result":{}}', '[]'):
            with self.subTest(body=body), self.assertRaises(ValueError):
                decode_response(body, 7)

    def test_fastmcp_list_and_analysis_detail_keep_their_shape(self):
        rows = [{"id": "analysis-id"}]
        detail = {"id": "analysis-id", "analysis_date": "2026-09-16"}
        self.assertEqual(tool_data({"structuredContent": {"result": rows}}), rows)
        self.assertEqual(tool_data({"structuredContent": detail}), detail)

    def test_text_only_and_empty_results_are_readable(self):
        self.assertEqual(tool_data({"content": [{"type": "text", "text": "[]"}]}), [])
        self.assertEqual(tool_data({"structuredContent": {}, "content": []}), {})


class DiagnosticTests(unittest.TestCase):
    def run_diagnostic(self, extra_tools=(), failing_tool=None):
        tools = [
            "list_analyses", "latest_analyses", "get_analysis",
            "get_recommendations", "suggest_ticker", "get_suggestion_status",
        ]
        calls = []

        def send(method, params, notification=False):
            if method == "initialize":
                return {"protocolVersion": "2025-03-26", "serverInfo": {"name": "Momentum Public"}}
            if method == "notifications/initialized":
                return None
            if method == "tools/list":
                return {"tools": [{"name": name} for name in [*tools, *extra_tools]]}
            self.assertEqual(method, "tools/call")
            name = params["name"]
            calls.append(name)
            if name == "latest_market_scan" or name == failing_tool:
                raise ValueError("isError=true : service unavailable")
            analysis = {"id": "998156cd-3427-4bcf-ac76-82a15b63208e", "analysis_date": "2026-08-02"}
            if name == "get_analysis":
                self.assertEqual(params["arguments"], {"analysis_id": analysis["id"]})
                return {"structuredContent": analysis}
            return {"structuredContent": {"result": [analysis]}}

        output = io.StringIO()
        with patch.object(check_mcp, "Client") as client, redirect_stdout(output):
            client.return_value.send.side_effect = send
            status = check_mcp.main()
        return status, calls, output.getvalue()

    def test_diagnostic_succeeds_with_only_supported_momentum_tools(self):
        status, calls, _ = self.run_diagnostic()
        self.assertEqual(status, 0)
        self.assertEqual(calls, ["list_analyses", "latest_analyses", "get_recommendations", "get_analysis"])

    def test_extra_unavailable_market_scan_is_never_called(self):
        status, calls, _ = self.run_diagnostic(extra_tools=("latest_market_scan",))
        self.assertEqual(status, 0)
        self.assertNotIn("latest_market_scan", calls)

    def test_supported_tool_failure_still_fails_the_diagnostic(self):
        status, calls, output = self.run_diagnostic(failing_tool="list_analyses")
        self.assertEqual(status, 1)
        self.assertIn("ÉCHEC list_analyses", output)
        self.assertIn("get_analysis", calls)


if __name__ == "__main__":
    unittest.main()
