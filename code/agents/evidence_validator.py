class EvidenceValidator:

    # Maps synonyms/keywords to canonical terms
    SYNONYMS = {
        "windshield": ["windshield", "front glass", "glass", "window"],
        "bumper": ["bumper", "front bumper", "rear bumper"],
        "headlight": ["headlight", "head light", "front light", "lamp"],
        "door": ["door", "door panel", "car door", "door trim"],
        "hood": ["hood", "bonnet"],
        "trunk": ["trunk", "boot", "rear"],
        "mirror": ["mirror", "side mirror", "wing mirror"],
        "tyre": ["tyre", "tire", "wheel"],
        "roof": ["roof", "top"],
        "seat": ["seat", "interior seat"],
    }

    def _normalize(self, text: str) -> str:
        """Find canonical key for any part string."""
        text = text.lower().strip()
        for canonical, variants in self.SYNONYMS.items():
            for v in variants:
                if v in text or text in v:
                    return canonical
        return text  # return as-is if no synonym found

    def validate(self, claim_data: dict, vision_results: list) -> dict:

        # Collect all visible parts from all images, normalized
        all_visible_raw = []
        for v in vision_results:
            parts = v.get("visible_parts", [])
            all_visible_raw.extend(parts)

        all_visible = [self._normalize(p) for p in all_visible_raw]

        # Parse claimed parts — split by comma or "and"
        affected_raw = claim_data.get("affected_part", "")
        # Replace " and " with comma, then split
        affected_raw = affected_raw.replace(" and ", ",")
        claimed_parts_raw = [
            p.strip() for p in affected_raw.split(",") if p.strip()
        ]
        claimed_parts = [self._normalize(p) for p in claimed_parts_raw]

        matched = []
        missing = []

        for part in claimed_parts:
            # Match if normalized form appears in visible list
            found = any(
                part in visible or visible in part or
                part == visible
                for visible in all_visible
            )
            if found:
                matched.append(part)
            else:
                missing.append(part)

        total = len(claimed_parts)
        match_ratio = len(matched) / total if total > 0 else 0

        # Sufficient if at least 50% of parts have evidence
        evidence_sufficient = match_ratio >= 0.5

        return {
            "evidence_sufficient": evidence_sufficient,
            "matched_parts": matched,
            "missing_parts": missing,
            "match_ratio": round(match_ratio, 2),
            "validation_reason": (
                "Evidence supports claim"
                if evidence_sufficient
                else f"Missing evidence for: {', '.join(missing)}"
            )
        }