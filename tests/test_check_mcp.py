import json
import unittest

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


if __name__ == "__main__":
    unittest.main()
