from agents.claim_extractor import ClaimExtractor
from agents.vision_inspector import VisionInspector
from agents.evidence_validator import EvidenceValidator
from agents.risk_assessor import RiskAssessor
from agents.decision_engine import DecisionEngine


class PipelineService:

    def __init__(self, loader, root):
        self.loader = loader
        self.root = root
        self.claim_extractor = ClaimExtractor()
        self.vision = VisionInspector()
        self.validator = EvidenceValidator()
        self.risk = RiskAssessor()
        self.decision = DecisionEngine()

    def process_claim(self, claim_row, history_df):
        claim_data = self.claim_extractor.extract(
            claim_row["user_claim"],
            claim_row["claim_object"]
        )

        image_paths = [
            str(self.root.parent / "dataset" / p)
            for p in claim_row["image_paths"].split(";")
        ]

        vision_results = self.vision.inspect_multiple(
            image_paths,
            claim_row["claim_object"]
        )

        validation = self.validator.validate(claim_data, vision_results)

        user_history = history_df[
            history_df["user_id"] == claim_row["user_id"]
        ].iloc[0]

        risk_result = self.risk.assess(user_history)

        decision = self.decision.decide(claim_data, validation, risk_result)

        return {
            "user_id": claim_row["user_id"],
            "image_paths": claim_row["image_paths"],
            "user_claim": claim_row["user_claim"],
            "claim_object": claim_row["claim_object"],
            "evidence_standard_met": validation["evidence_sufficient"],
            "evidence_standard_met_reason": validation["validation_reason"],
            "risk_flags": ", ".join(risk_result["risk_flags"]) if risk_result["risk_flags"] else "none",
            "issue_type": claim_data.get("issue", ""),
            "object_part": claim_data.get("affected_part", ""),
            "claim_status": decision["decision"],
            "claim_status_justification": decision["reason"],
            "supporting_image_ids": ", ".join([
                p.split("/")[-1] for p in claim_row["image_paths"].split(";")
            ]),
            "valid_image": any(v.get("damage_found", False) for v in vision_results),
            "severity": claim_data.get("severity", "")
        }