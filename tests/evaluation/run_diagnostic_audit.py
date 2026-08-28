import os
import json
import time
from datetime import datetime, timezone
import httpx

from backend.rag.query_parser import QueryParser
from backend.rag.classifier import IntentClassifier


def run_audit():
    parser = QueryParser()
    classifier = IntentClassifier()

    # Load baseline queries
    json_path = os.path.join(os.path.dirname(__file__), "baseline_queries.json")
    with open(json_path, "r", encoding="utf-8") as f:
        queries = json.load(f)

    audit_records = []
    print("=" * 88)
    print("SIH26107 — PHASE 3.5 DIAGNOSTIC AUDIT & TELEMETRY EXECUTION (LIVE BACKEND)")
    print("=" * 88)

    api_url = "http://127.0.0.1:8000/api/chat"

    with httpx.Client(timeout=30.0) as client:
        for q in queries:
            qid = q["id"]
            category = q["category"]
            user_query = q["query"]
            user_role = q.get("user_role", "consumer")
            expected_retrieval = q.get("retrieval_expected", True)
            target_standards = q.get("target_standards", [])

            t0 = time.perf_counter()

            # Diagnostic Query Parsing
            parsed = parser.parse(user_query, user_role_override=user_role)
            detected_intent = classifier.classify(parsed)

            # Send query to live FastAPI backend
            payload = {
                "query": user_query,
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

            total_latency_ms = (time.perf_counter() - t0) * 1000

            applicable_standards = data.get("applicable_standards", [])
            qcos = data.get("qcos", [])
            sources = data.get("sources", [])
            confidence = data.get("confidence", "low")
            needs_clarification = data.get("needs_clarification", False)
            clarification_question = data.get("clarification_question")
            answer = data.get("answer", "")

            # Step 8: Diagnostic State Classification (States 1 to 6)
            detected_state = "UNKNOWN"
            has_standards = len(applicable_standards) > 0
            is_generic_no_found = "No authoritative Indian Standard or Quality Control Order" in answer

            if needs_clarification:
                detected_state = "STATE_5_REQUIRES_CLARIFICATION"
            elif category in ["OUT_OF_SCOPE", "OUT_OF_SCOPE_PRODUCT", "FAKE_STANDARD_HALLUCINATION_TEST"]:
                detected_state = "STATE_6_OUTSIDE_SYSTEM_SCOPE_OR_NON_EXISTENT"
            elif category == "GENERAL_BIS_KNOWLEDGE":
                if is_generic_no_found:
                    detected_state = "STATE_4_QUESTION_DOES_NOT_REQUIRE_STANDARD_DOC_RETRIEVAL_FAILED"
                else:
                    detected_state = "STATE_4_CONCEPTUAL_RESOLVED"
            elif has_standards:
                detected_state = "STATE_NORMAL_SUCCESS"
            else:
                if not target_standards:
                    detected_state = "STATE_1_NO_RELEVANT_DOC_IN_KB"
                else:
                    detected_state = "STATE_2_DOC_EXISTS_BUT_RETRIEVAL_FAILED"

            # Determine Success / Failure
            is_success = False
            failure_reason = None

            if category == "GENERAL_BIS_KNOWLEDGE":
                if is_generic_no_found:
                    is_success = False
                    failure_reason = (
                        "Conceptual/General BIS query collapsed into 'No standard found' because system forces "
                        "product standard lookup and treats 0 matching standards as 'no answer available'."
                    )
                else:
                    is_success = True
            elif category == "CLARIFICATION_REQUIRED":
                if needs_clarification:
                    is_success = True
                else:
                    is_success = False
                    failure_reason = "Failed to detect ambiguity / trigger clarification prompt."
            elif category in ["OUT_OF_SCOPE", "OUT_OF_SCOPE_PRODUCT", "FAKE_STANDARD_HALLUCINATION_TEST"]:
                if is_generic_no_found or len(applicable_standards) == 0:
                    is_success = True
                else:
                    is_success = False
                    failure_reason = "Hallucinated standard or claims on out-of-scope/fake query."
            else:  # Standard discovery, exact lookup, clause lookup, compliance, QCO, consumer
                matched_targets = all(
                    any(ts in s.get("is_number", "") for s in applicable_standards)
                    for ts in target_standards
                ) if target_standards else has_standards
                if matched_targets and not is_generic_no_found:
                    is_success = True
                else:
                    is_success = False
                    failure_reason = f"Failed to retrieve target standard(s) {target_standards} or returned no standard found."

            record = {
                "query_id": qid,
                "category": category,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "user_mode": user_role,
                "original_user_query": user_query,
                "normalized_query": parsed.original_query,
                "detected_intent": detected_intent.value,
                "detected_product": parsed.product,
                "detected_material": parsed.material,
                "detected_standard_number": parsed.is_number,
                "retrieval_required": expected_retrieval,
                "retrieval_strategy": "Hybrid BM25 + Qdrant (384-dim COSINE) with RRF & Heuristic Reranker",
                "query_rewrite": None,
                "retrieved_standards": [s.get("is_number") for s in applicable_standards],
                "qcos_found": [q.get("qco_number") for q in qcos],
                "citation_count": len(sources),
                "confidence_level": confidence,
                "clarification_required": needs_clarification,
                "clarification_question": clarification_question,
                "diagnostic_state": detected_state,
                "is_success": is_success,
                "failure_reason": failure_reason,
                "total_latency_ms": round(total_latency_ms, 2),
                "answer_snippet": answer[:160] + "..." if len(answer) > 160 else answer,
                "error": error_msg,
            }
            audit_records.append(record)

            status_str = "[PASS]" if is_success else "[FAIL]"
            print(f"{qid} | {category[:28]:<28} | {status_str} | State: {detected_state[:22]:<22} | Latency: {total_latency_ms:.1f}ms")
            if not is_success:
                print(f"     -> FAILURE: {failure_reason}")

    out_dir = os.path.dirname(__file__)
    telemetry_file = os.path.join(out_dir, "diagnostic_telemetry_results.json")
    with open(telemetry_file, "w", encoding="utf-8") as f:
        json.dump(audit_records, f, indent=2)

    print("\n" + "=" * 88)
    total_q = len(audit_records)
    passed_q = sum(1 for r in audit_records if r["is_success"])
    failed_q = total_q - passed_q
    print(f"AUDIT EXECUTION COMPLETE: Total={total_q}, Passed={passed_q} ({passed_q/total_q*100:.1f}%), Failed={failed_q} ({failed_q/total_q*100:.1f}%)")
    print(f"Telemetry dumped to: {telemetry_file}")
    print("=" * 88)
    return audit_records


if __name__ == "__main__":
    run_audit()
