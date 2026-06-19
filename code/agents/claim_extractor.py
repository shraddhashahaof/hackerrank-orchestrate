import json
from utils.llm_factory import LLMFactory
from utils.logger import logger
from utils import cache, retry


class ClaimExtractor:

    def __init__(self):
        self.client = LLMFactory.get_client()

    def extract(self, user_claim: str, claim_object: str) -> dict:
        prompt = f"""
You are an insurance claim extraction agent.

Extract structured information from this claim:

Claim: "{user_claim}"
Object: "{claim_object}"

IMPORTANT RULES:
- affected_part must be a comma-separated list of individual parts
- Do NOT use "and" to join parts — use commas only
- Example: "front bumper, left headlight" not "front bumper and left headlight"
- Use simple generic part names: "door", "windshield", "bumper", "headlight"
- Do NOT include qualifiers in brackets — just say "windshield" not "front glass (windshield)"

Respond ONLY with valid JSON:
{{
  "issue": "damage type",
  "affected_part": "part1, part2",
  "summary": "brief summary",
  "severity": "low|medium|high"
}}

No explanation. JSON only.
"""
        cached = cache.get(prompt)
        if cached:
            return cached

        def call():
            response = self.client.generate(prompt)
            clean = response.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(clean)

        try:
            result = retry.with_retry(call)
            cache.set(prompt, result)
            logger.info(f"ClaimExtractor: {result}")
            return result
        except Exception as e:
            logger.error(f"ClaimExtractor failed: {e}")
            return {
                "issue": "unknown",
                "affected_part": "",
                "summary": str(e),
                "severity": "low"
            }