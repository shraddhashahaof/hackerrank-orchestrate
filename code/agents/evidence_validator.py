class EvidenceValidator:

    def validate(
        self,
        claim_extraction,
        vision_results,
        evidence_rule=None
    ):

        claimed_parts = [
            part.strip().lower()
            for part in claim_extraction[
                "affected_part"
            ].split(",")
        ]

        visible_parts = []

        for result in vision_results:

            part = (
                result.get(
                    "affected_part",
                    ""
                )
                .strip()
                .lower()
            )

            if part and part != "none":

                visible_parts.append(part)

        matched_parts = []

        missing_parts = []

        for claimed in claimed_parts:

            found = False

            for visible in visible_parts:

                if claimed in visible or visible in claimed:

                    found = True
                    break

            if found:

                matched_parts.append(
                    claimed
                )

            else:

                missing_parts.append(
                    claimed
                )

        evidence_sufficient = (
            len(missing_parts) == 0
        )

        if evidence_sufficient:

            reason = (
                "All claimed parts have visual evidence"
            )

        else:

            reason = (
                "Missing evidence for: "
                + ", ".join(missing_parts)
            )

        return {
            "evidence_sufficient":
            evidence_sufficient,

            "matched_parts":
            matched_parts,

            "missing_parts":
            missing_parts,

            "validation_reason":
            reason
        }