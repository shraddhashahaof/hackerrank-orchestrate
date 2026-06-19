import json
from utils.llm_factory import LLMFactory


class VisionInspector:

    def __init__(self):
        self.client = LLMFactory.get_client()

    def inspect(self, image_path: str, claim_object: str) -> dict:
        prompt = f"""
You are an insurance claim image inspector.

Inspect this image of a {claim_object} and identify all visible damage or issues.

Respond ONLY with valid JSON like this:
{{
  "visible_parts": ["front bumper", "left headlight"],
  "damage_found": true,
  "damage_description": "Dent on front bumper, cracked left headlight"
}}

No explanation. JSON only.
"""
        try:
            response = self.client.generate_vision(prompt, image_path)
            clean = response.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(clean)
        except Exception as e:
            return {
                "visible_parts": [],
                "damage_found": False,
                "damage_description": f"Inspection failed: {e}"
            }

    def inspect_multiple(self, image_paths: list, claim_object: str) -> list:
        results = []
        for path in image_paths:
            result = self.inspect(path, claim_object)
            results.append(result)
        return results