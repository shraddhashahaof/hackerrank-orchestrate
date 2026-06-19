class DecisionEngine:

    def decide(
        self,
        claim_data,
        validation_result,
        risk_result
    ):

        evidence_ok = validation_result[
            "evidence_sufficient"
        ]

        risk_level = risk_result[
            "risk_level"
        ]

        if evidence_ok and risk_level == "low":

            return {
                "decision": "approve",
                "confidence": 0.90,
                "reason": (
                    "Evidence supports claim "
                    "and risk is low"
                )
            }

        if evidence_ok and risk_level == "medium":

            return {
                "decision": "manual_review",
                "confidence": 0.75,
                "reason": (
                    "Evidence supports claim "
                    "but risk requires review"
                )
            }

        if not evidence_ok:

            return {
                "decision": "reject",
                "confidence": 0.85,
                "reason": validation_result[
                    "validation_reason"
                ]
            }

        return {
            "decision": "manual_review",
            "confidence": 0.50,
            "reason": "Unable to determine"
        }