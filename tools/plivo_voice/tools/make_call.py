from typing import Any, Generator

import plivo
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# Plivo's own hosted sample XML. It answers the call and speaks a short message,
# so the tool places a working call with no extra setup. Anything beyond a
# confirmation call should point answer_url at a URL serving its own Plivo XML.
DEFAULT_ANSWER_URL = "https://s3.amazonaws.com/static.plivo.com/answer.xml"


class MakeCallTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        to_number = str(tool_parameters.get("to_number") or "").strip()
        from_number = str(tool_parameters.get("from_number") or "").strip()
        answer_url = (
            str(tool_parameters.get("answer_url") or "").strip() or DEFAULT_ANSWER_URL
        )
        answer_method = (
            str(tool_parameters.get("answer_method") or "").strip().upper() or "POST"
        )

        if not to_number or not from_number:
            yield from self._fail(
                "Both to_number and from_number are required, in E.164 format.",
                to_number,
                from_number,
            )
            return

        if answer_method not in ("GET", "POST"):
            yield from self._fail(
                f"Invalid answer_method '{answer_method}'. Must be GET or POST.",
                to_number,
                from_number,
            )
            return

        try:
            auth_id = self.runtime.credentials["auth_id"]
            auth_token = self.runtime.credentials["auth_token"]
        except KeyError as e:
            yield from self._fail(
                f"Missing Plivo credential: {e}. Configure the plugin before using it.",
                to_number,
                from_number,
            )
            return

        try:
            client = plivo.RestClient(auth_id=auth_id, auth_token=auth_token)
            response = client.calls.create(
                from_=from_number,
                to_=to_number,
                answer_url=answer_url,
                answer_method=answer_method,
            )
            request_uuid = getattr(response, "request_uuid", "unknown")
        except plivo.exceptions.AuthenticationError:
            yield from self._fail(
                "Plivo authentication failed. Please check your credentials.",
                to_number,
                from_number,
            )
            return
        except plivo.exceptions.ValidationError as e:
            yield from self._fail(
                f"Invalid request parameters: {e}", to_number, from_number
            )
            return
        except plivo.exceptions.PlivoRestError as e:
            yield from self._fail(f"Plivo API error: {e}", to_number, from_number)
            return
        except Exception as e:
            yield from self._fail(
                f"An unexpected error occurred: {e}", to_number, from_number
            )
            return

        yield self.create_text_message(
            f"Call initiated successfully to {to_number}. Request UUID: {request_uuid}"
        )
        yield self.create_json_message({
            "status": "success",
            "request_uuid": request_uuid,
            "to": to_number,
            "from": from_number,
            "answer_url": answer_url,
            "answer_method": answer_method,
        })

    def _fail(
        self, message: str, to_number: str, from_number: str
    ) -> Generator[ToolInvokeMessage, None, None]:
        """Every failure path reports the same way, in text and as structured JSON."""
        yield self.create_text_message(message)
        yield self.create_json_message({
            "status": "failed",
            "to": to_number,
            "from": from_number,
            "error": message,
        })
