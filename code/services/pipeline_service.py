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
            "claim_object": claim_row["claim_object"],
            "decision": decision["decision"],
            "confidence": decision["confidence"],
            "reason": decision["reason"]
        }