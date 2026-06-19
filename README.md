# 🛡️ Orchestrate — AI-Powered Insurance Claim Processing Pipeline

> HackerRank Hackathon — June 2026
> Multi-Agent Orchestration System for Automated Insurance Claim Decisions

---

## 📌 What This Project Does

Orchestrate is a **multi-agent AI pipeline** that processes insurance claims end-to-end:

1. Extracts structured data from unstructured claim conversations
2. Inspects claim images using vision AI
3. Validates evidence against claimed damage
4. Assesses user risk from claim history
5. Makes a final decision: **approve / manual_review / reject**

All decisions are **traceable and explainable** — every output includes a confidence score and reason.

---

## 🏗️ Architecture

```
User Claim (text + images)
        │
        ▼
┌─────────────────┐
│  ClaimExtractor │  ← Extracts: issue, affected_part, severity
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ VisionInspector │  ← Inspects images: visible_parts, damage_found
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  EvidenceValidator   │  ← Matches vision findings to claimed parts
└────────┬─────────────┘
         │
         ▼
┌─────────────────┐
│  RiskAssessor   │  ← Scores user based on claim history
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ DecisionEngine  │  ← Combines all signals → final decision
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Evaluator     │  ← Reports metrics on all processed claims
└─────────────────┘
```

---

## 📁 Project Structure

```
code/
├── agents/
│   ├── claim_extractor.py      # LLM-based claim parsing
│   ├── vision_inspector.py     # Vision API image analysis
│   ├── evidence_validator.py   # Fuzzy part matching
│   ├── risk_assessor.py        # User risk scoring
│   └── decision_engine.py      # Final decision logic
│
├── utils/
│   ├── groq_client.py          # Groq API wrapper (text + vision)
│   ├── llm_factory.py          # Provider abstraction
│   ├── logger.py               # Structured logging
│   ├── cache.py                # MD5-keyed response cache
│   └── retry.py                # Exponential retry wrapper
│
├── services/
│   └── pipeline_service.py     # Orchestrates all agents per claim
│
├── evaluation/
│   └── evaluator.py            # Metrics: accuracy, distribution, confidence
│
├── tests/
│   ├── test_groq.py
│   ├── test_vision.py
│   ├── test_pipeline.py
│   ├── test_decision.py
│   ├── test_evaluation.py
│   └── test_debug.py
│
├── outputs/
│   └── results.csv             # Pipeline output (auto-generated)
│
├── logs/
│   └── pipeline.log            # Full execution log (auto-generated)
│
├── main.py                     # Entry point
├── data_loader.py              # Loads claims + user history CSVs
└── config.py                   # API keys, provider config
```

---

## ⚙️ Setup

### 1. Clone & enter project
```bash
git clone https://github.com/shraddhashahaof/hackerrank-orchestrate.git
cd hackerrank-orchestrate/code
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install groq pandas python-dotenv
```

### 4. Create `.env` file
```
GROQ_API_KEY=your_groq_api_key_here
PROVIDER=groq
```

### 5. Add Dataset
Download the dataset from the official HackerRank repo and place it in the repo root:

👉 [Download Dataset](https://github.com/interviewstreet/hackerrank-orchestrate-june26/tree/main/dataset)

Place it as:
```
hackerrank-orchestrate/
└── dataset/
    ├── claims.csv
    ├── user_history.csv
    ├── evidence_requirements.csv
    └── images/
        ├── sample/
        └── test/
```

---

## 🚀 Run

### Full pipeline (all claims)
```bash
python main.py
```

### Individual tests
```bash
python tests\test_groq.py        # Test LLM connection
python tests\test_vision.py      # Test image inspection
python tests\test_pipeline.py    # Test 3 claims end-to-end
python tests\test_evaluation.py  # Show metrics report
python tests\test_debug.py       # Verbose output per claim
```

---

## 📊 Sample Output

```
2026-06-20 01:49:34 [INFO] orchestrate — ==================================================
2026-06-20 01:49:34 [INFO] orchestrate —   ORCHESTRATE — Insurance Claim AI Pipeline
2026-06-20 01:49:34 [INFO] orchestrate — ==================================================
2026-06-20 01:49:34 [INFO] orchestrate — Loaded 44 claims | 47 user history records
2026-06-20 01:49:35 [INFO] orchestrate — [1/44] Processing user=user_002 object=car
2026-06-20 01:49:35 [INFO] orchestrate — ClaimExtractor: {'issue': 'accident', 'affected_part': 'bumper, headlight', 'summary': 'Damage to car after parking near office', 'severity': 'medium'}
2026-06-20 01:49:36 [INFO] orchestrate —   → decision=approve | confidence=0.68 | reason=Evidence supports claim (50% parts matched) and risk is low

.....
.....
.....

==================================================
   ORCHESTRATE PIPELINE — EVALUATION REPORT
==================================================
  Total Claims Processed : 44
  Avg Confidence Score   : 0.849

  Decision Distribution:
    ✅ Approved      : 10  (22.7%)
    🔍 Manual Review : 2  (4.5%)
    ❌ Rejected      : 32  (72.7%)
==================================================

```

---

## 🧠 Models Used

| Task | Model | Provider |
|------|-------|----------|
| Claim Extraction | llama-3.1-8b-instant | Groq |
| Risk Assessment | llama-3.1-8b-instant | Groq |
| Image Inspection | meta-llama/llama-4-scout-17b-16e-instruct | Groq |

---

## 🔑 Key Design Decisions

- **LLMFactory** — swap providers (Groq/Gemini) without touching agent code
- **Fuzzy matching** — "car door" matches "door panel" via synonym dictionary
- **Cache layer** — identical prompts never hit the API twice
- **Retry logic** — 3 attempts with 2s delay on API failures
- **Structured logging** — every decision logged to `logs/pipeline.log`

---

## 👩‍💻 Author

Shraddha Shaha — HackerRank Orchestrate Hackathon, June 2026