from typing import Any, Generator

import plivo
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class MakeCallTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        to_number = tool_parameters["to_number"].strip()
        from_number = tool_parameters["from_number"].strip()
        answer_url = tool_parameters["answer_url"].strip()
        answer_method = (tool_parameters.get("answer_method") or "").strip().upper()

        if not answer_method:
            answer_method = "POST"
        elif answer_method not in ("GET", "POST"):
            yield self.create_text_message(
                f"Invalid answer_method '{answer_method}'. Must be GET or POST."
            )
            yield self.create_json_message({
                "status": "failed",
                "to": to_number,
                "from": from_number,
                "error": f"Invalid answer_method '{answer_method}'. Must be GET or POST.",
            })
            return

        auth_id = self.runtime.credentials["auth_id"]
        auth_token = self.runtime.credentials["auth_token"]

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
            yield self.create_text_message(
                "Plivo authentication failed. Please check your credentials."
            )
            yield self.create_json_message({
                "status": "failed",
                "to": to_number,
                "from": from_number,
                "error": "Plivo authentication failed. Please check your credentials.",
            })
            return
        except plivo.exceptions.ValidationError as e:
            yield self.create_text_message(f"Invalid request parameters: {e}")
            yield self.create_json_message({
                "status": "failed",
                "to": to_number,
                "from": from_number,
                "error": str(e),
            })
            return
        except plivo.exceptions.PlivoRestError as e:
            yield self.create_text_message(f"Plivo API error: {e}")
            yield self.create_json_message({
                "status": "failed",
                "to": to_number,
                "from": from_number,
                "error": str(e),
            })
            return
        except Exception as e:
            yield self.create_text_message(f"An unexpected error occurred: {e}")
            yield self.create_json_message({
                "status": "failed",
                "to": to_number,
                "from": from_number,
                "error": str(e),
            })
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
