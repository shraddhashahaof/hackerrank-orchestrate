import json
from pathlib import Path
from utils.llm_factory import LLMFactory


class VisionInspector:

    def __init__(self):
        self.client = LLMFactory.get_client()

    def inspect(self, image_path: str, claim_object: str) -> dict:
        # Skip if file doesn't exist or is too small (likely corrupt)
        path = Path(image_path)
        if not path.exists() or path.stat().st_size < 1000:
            return {
                "visible_parts": [],
                "damage_found": False,
                "damage_description": "Image unavailable or too small"
            }

        prompt = f"""
You are an insurance claim image inspector.

Inspect this image of a {claim_object} and identify all visible damage or issues.

Respond ONLY with valid JSON:
{{
  "visible_parts": ["part1", "part2"],
  "damage_found": true,
  "damage_description": "brief description"
}}

Use simple part names like: bumper, headlight, door, windshield, hood, mirror, tyre, roof.
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