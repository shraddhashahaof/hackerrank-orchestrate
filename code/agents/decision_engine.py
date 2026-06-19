class DecisionEngine:

    def decide(
        self,
        claim_data: dict,
        validation_result: dict,
        risk_result: dict
    ) -> dict:

        evidence_ok = validation_result["evidence_sufficient"]
        risk_level = risk_result["risk_level"]
        risk_score = risk_result.get("risk_score", 0)
        match_ratio = validation_result.get("match_ratio", 0)

        # Confidence based on match ratio and risk score
        base_confidence = round(
            0.5 + (match_ratio * 0.35) - (risk_score * 0.05), 2
        )
        base_confidence = max(0.50, min(0.97, base_confidence))

        if evidence_ok and risk_level == "low":
            return {
                "decision": "approve",
                "confidence": base_confidence,
                "reason": (
                    f"Evidence supports claim "
                    f"({int(match_ratio*100)}% parts matched) "
                    f"and risk is low"
                )
            }

        if evidence_ok and risk_level == "medium":
            return {
                "decision": "manual_review",
                "confidence": round(base_confidence - 0.10, 2),
                "reason": (
                    "Evidence supports claim "
                    "but risk level requires manual review"
                )
            }

        if evidence_ok and risk_level == "high":
            return {
                "decision": "manual_review",
                "confidence": round(base_confidence - 0.15, 2),
                "reason": "Evidence present but high risk profile"
            }

        if not evidence_ok and match_ratio >= 0.3:
            return {
                "decision": "manual_review",
                "confidence": round(0.50 + match_ratio * 0.15, 2),
                "reason": (
                    f"Partial evidence only — "
                    f"{validation_result['validation_reason']}"
                )
            }

        return {
            "decision": "reject",
            "confidence": round(0.75 + (1 - match_ratio) * 0.15, 2),
            "reason": validation_result["validation_reason"]
        }