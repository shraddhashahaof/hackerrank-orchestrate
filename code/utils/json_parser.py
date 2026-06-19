import json


def parse_json_response(response_text: str):

    try:
        return json.loads(response_text)

    except Exception:

        start = response_text.find("{")
        end = response_text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                f"Unable to locate JSON in:\n{response_text}"
            )

        cleaned = response_text[start:end + 1]

        return json.loads(cleaned)