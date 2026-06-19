class RiskAssessor:

    def assess(
        self,
        user_history_row
    ):

        risk_score = 0

        risk_flags = []

        if user_history_row[
            "last_90_days_claim_count"
        ] >= 3:

            risk_score += 30

            risk_flags.append(
                "high_recent_claim_frequency"
            )

        if user_history_row[
            "rejected_claim"
        ] >= 2:

            risk_score += 25

            risk_flags.append(
                "multiple_rejected_claims"
            )

        if user_history_row[
            "manual_review_claim"
        ] >= 2:

            risk_score += 20

            risk_flags.append(
                "multiple_manual_reviews"
            )

        history_flags = str(
            user_history_row[
                "history_flags"
            ]
        ).lower()

        if (
            "fraud" in history_flags
            or "exaggerated" in history_flags
        ):

            risk_score += 40

            risk_flags.append(
                "historical_risk_flag"
            )

        if risk_score < 30:

            risk_level = "low"

        elif risk_score < 60:

            risk_level = "medium"

        else:

            risk_level = "high"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_flags": risk_flags
        }