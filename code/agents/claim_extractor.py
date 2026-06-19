from utils.gemini_client import GeminiClient
from utils.json_parser import parse_json_response


class ClaimExtractor:

    def __init__(self):

        self.client = GeminiClient()

    def extract(
        self,
        claim_text: str,
        claim_object: str
    ):

        prompt = f"""
You are an insurance claim analyst.

Claim Object:
{claim_object}

Claim Description:
{claim_text}

Extract:

1. issue
2. affected_part
3. summary
4. severity

Severity must be one of:

low
medium
high

Return ONLY JSON.

Example:

{{
    "issue":"crack",
    "affected_part":"windshield",
    "summary":"Front windshield cracked by road debris",
    "severity":"medium"
}}
"""

        response = self.client.generate(prompt)

        return parse_json_response(response)