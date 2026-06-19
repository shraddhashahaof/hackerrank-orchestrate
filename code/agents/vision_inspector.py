from utils.gemini_client import GeminiClient
from utils.json_parser import parse_json_response
from utils.image_utils import load_image


class VisionInspector:

    def __init__(self):
        self.client = GeminiClient()

    def inspect(
        self,
        image_path,
        claim_object
    ):

        image = load_image(image_path)

        prompt = f"""
You are an insurance image reviewer.

Expected object:
{claim_object}

Analyze image carefully.

Return ONLY valid JSON.

{{
    "object":"car",
    "visible_damage":"scratch",
    "affected_part":"front bumper",
    "image_quality":"good",
    "damage_visible":true
}}

Rules:
- object must identify what is visible
- visible_damage should be concise
- affected_part should identify damaged area
- image_quality must be: good, medium, poor
- damage_visible must be true or false
"""

        response = self.client.generate_vision(
            prompt,
            image
        )

        return parse_json_response(response)

    def inspect_multiple(
        self,
        image_paths,
        claim_object
    ):

        results = []

        for image_path in image_paths:

            try:

                result = self.inspect(
                    image_path=image_path,
                    claim_object=claim_object
                )

                results.append(result)

            except Exception as e:

                print(
                    f"Failed on {image_path}: {e}"
                )

        return results