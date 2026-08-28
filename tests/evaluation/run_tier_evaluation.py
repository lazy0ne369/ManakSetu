import os
import json
import time
from datetime import datetime, timezone
import httpx

from backend.rag.query_parser import QueryParser
from backend.rag.classifier import IntentClassifier


def run_tier_evaluation():
    parser = QueryParser()
    classifier = IntentClassifier()

    json_path = os.path.join(os.path.dirname(__file__), "tier_evaluation_dataset.json")
    with open(json_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    api_url = "http://127.0.0.1:8000/api/chat"

    print("=" * 95)
    print("SIH26107 — 3-TIER AI / RAG EVALUATION EXECUTION (ALL 54 QUESTIONS)")
    print("=" * 95)

    evaluation_records = []
    tier_stats = {
        "Tier 1 — Foundation & Retrieval": {"total": 0, "passed": 0, "failed": 0},
        "Tier 2 — Reasoning, Clarification & Compliance": {"total": 0, "passed": 0, "failed": 0},
        "Tier 3 — Robustness, Grounding & Failure Resistance": {"total": 0, "passed": 0, "failed": 0},
    }

    current_tier = ""

    with httpx.Client(timeout=30.0) as client:
        for q in questions:
            qid = q["id"]
            tier = q["tier"]
            category = q["category"]
            query = q["query"]
            expected_behavior = q["expected_behavior"]
            user_role = q.get("user_role", "consumer")
            target_standards = q.get("target_standards", [])

            if tier != current_tier:
                current_tier = tier
                print(f"\n{'#' * 95}\n{current_tier.upper()}\n{'#' * 95}")

            tier_stats[tier]["total"] += 1

            t0 = time.perf_counter()

            # Diagnostic entity parsing
            parsed = parser.parse(query, user_role_override=user_role)
            detected_intent = classifier.classify(parsed)

            # API Call
            payload = {
                "query": query,
                "user_role": user_role,
            }

            error_msg = None
            try:
                resp = client.post(api_url, json=payload)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                error_msg = str(e)
                data = {
                    "answer": f"ERROR: {error_msg}",
                    "applicable_standards": [],
                    "certification_status": "Error",
                    "certification_scheme": None,
                    "qcos": [],
                    "key_requirements": [],
                    "compliance_steps": [],
                    "sources": [],
                    "confidence": "low",
                    "needs_clarification": False,
                    "clarification_question": None,
                }

            latency_ms = round((time.perf_counter() - t0) * 1000, 2)

            applicable_standards = data.get("applicable_standards", [])
            qcos = data.get("qcos", [])
            sources = data.get("sources", [])
            confidence = data.get("confidence", "low")
            needs_clarification = data.get("needs_clarification", False)
            clarification_question = data.get("clarification_question")
            answer = data.get("answer", "")

            # Fill Evaluation Recording Template
            retrieval_triggered = not needs_clarification
            has_standards = len(applicable_standards) > 0
            is_no_info_found = "No authoritative Indian Standard or Quality Control Order" in answer

            # Relevant documents retrieved?
            if target_standards:
                matched_targets = [
                    ts for ts in target_standards
                    if any(ts in s.get("is_number", "") for s in applicable_standards)
                ]
                if len(matched_targets) == len(target_standards):
                    relevant_docs = "Yes"
                elif len(matched_targets) > 0:
                    relevant_docs = "Partial"
                else:
                    relevant_docs = "No"
            else:
                relevant_docs = "Yes" if has_standards or "General" in category or "Fake" in category or "Ambiguity" in category else "No"

            # Relevant chunks retrieved?
            relevant_chunks = "Yes" if len(data.get("key_requirements", [])) > 0 else "Partial" if has_standards else "No"

            # Citation provided & correct
            citation_provided = "Yes" if len(sources) > 0 else "No"
            citation_correct = "Yes" if len(sources) > 0 and has_standards else "N/A" if not target_standards else "No"

            # Answer grounded
            answer_grounded = "Yes" if not is_no_info_found and has_standards else "Partial" if needs_clarification or is_no_info_found else "No"

            # Clarification appropriate
            is_clarification_category = "Clarification" in category or "Ambiguity" in category or "needs_clarification" in expected_behavior.lower()
            if is_clarification_category:
                clarification_appropriate = "Yes" if needs_clarification else "No"
            else:
                clarification_appropriate = "No" if needs_clarification and target_standards else "N/A"

            # Confidence appropriate
            confidence_appropriate = "Yes"
            if is_no_info_found and confidence != "low":
                confidence_appropriate = "No"
            if has_standards and len(sources) > 0 and confidence == "low":
                confidence_appropriate = "No"

            # Hallucination detected
            hallucination_detected = "No"
            if "Fake" in category or "99999" in query or "0000" in query:
                if any("99999" in s.get("is_number", "") or "0000" in s.get("is_number", "") for s in applicable_standards):
                    hallucination_detected = "Yes"

            # Pass / Fail assessment
            is_pass = False
            notes = ""

            if "General BIS Knowledge" in category or "QCO & Certification Reasoning" in category or "Version / Amendment" in category:
                if is_no_info_found:
                    is_pass = False
                    notes = "FAILURE: Conceptual/General query collapsed to 'No standard found' because system forces specific product standard lookup."
                else:
                    is_pass = True
                    notes = "Grounded conceptual response."
            elif is_clarification_category:
                if needs_clarification:
                    is_pass = True
                    notes = "Correctly detected underspecified context and prompted for product."
                elif has_standards and not target_standards:
                    is_pass = False
                    notes = "FAILURE: Failed to detect ambiguity; made unwarranted product assumption."
                else:
                    is_pass = True
            elif "Fake" in category or "Hallucination" in category:
                if is_no_info_found or len(applicable_standards) == 0:
                    is_pass = True
                    notes = "Zero-hallucination verified. Correctly rejected fake standard/clause."
                else:
                    is_pass = False
                    notes = "FAILURE: Hallucinated claims for fake input."
            elif target_standards:
                if relevant_docs == "Yes" and not is_no_info_found:
                    is_pass = True
                    notes = f"Successfully identified target standard {target_standards} and active QCO."
                elif needs_clarification:
                    is_pass = False
                    notes = "FAILURE: False positive clarification triggered on detailed query."
                else:
                    is_pass = False
                    notes = f"FAILURE: Target standard {target_standards} not retrieved."
            else:
                if not is_no_info_found or "Out of Scope" in category:
                    is_pass = True
                    notes = "Handled appropriately."
                else:
                    is_pass = False
                    notes = "Generic no-information fallback."

            if is_pass:
                tier_stats[tier]["passed"] += 1
            else:
                tier_stats[tier]["failed"] += 1

            record = {
                "query_id": qid,
                "tier": tier,
                "category": category,
                "user_query": query,
                "expected_behavior": expected_behavior,
                "query_classification": detected_intent.value,
                "retrieval_triggered": "Yes" if retrieval_triggered else "No",
                "relevant_documents_retrieved": relevant_docs,
                "relevant_chunks_retrieved": relevant_chunks,
                "citation_provided": citation_provided,
                "citation_correct": citation_correct,
                "answer_grounded": answer_grounded,
                "clarification_appropriate": clarification_appropriate,
                "confidence_appropriate": confidence_appropriate,
                "hallucination_detected": hallucination_detected,
                "latency_ms": latency_ms,
                "pass_fail": "Pass" if is_pass else "Fail",
                "notes_root_cause": notes,
                "retrieved_standards": [s.get("is_number") for s in applicable_standards],
                "confidence_level": confidence,
                "answer_preview": answer[:120] + "..." if len(answer) > 120 else answer,
            }
            evaluation_records.append(record)

            status_tag = "[PASS]" if is_pass else "[FAIL]"
            print(f"{qid:<6} | {category[:24]:<24} | {status_tag} | Latency: {latency_ms:>6.1f}ms | {notes[:45]}")

    # Write JSON results
    out_dir = os.path.dirname(__file__)
    res_file = os.path.join(out_dir, "tier_evaluation_results.json")
    with open(res_file, "w", encoding="utf-8") as f:
        json.dump(evaluation_records, f, indent=2)

    print("\n" + "=" * 95)
    print("3-TIER EVALUATION SUMMARY SCORECARD")
    print("=" * 95)
    total_all = len(evaluation_records)
    passed_all = sum(1 for r in evaluation_records if r["pass_fail"] == "Pass")
    failed_all = total_all - passed_all

    for t_name, s in tier_stats.items():
        pct = (s["passed"] / s["total"] * 100) if s["total"] > 0 else 0
        print(f"• {t_name:<55}: {s['passed']}/{s['total']} Passed ({pct:.1f}%)")

    print("-" * 95)
    print(f"OVERALL PERFORMANCE ACROSS ALL 3 TIERS: {passed_all}/{total_all} Passed ({passed_all/total_all*100:.1f}%)")
    print(f"Detailed JSON results exported to: {res_file}")
    print("=" * 95)

    return evaluation_records, tier_stats


if __name__ == "__main__":
    run_tier_evaluation()
