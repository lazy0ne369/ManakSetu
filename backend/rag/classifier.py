import re
from backend.rag.schemas import QueryIntent, ParsedQuery


class IntentClassifier:
    def classify(self, parsed: ParsedQuery) -> QueryIntent:
        text = parsed.original_query.lower()

        # Check for comparison
        if "compare" in text or "difference between" in text or "vs" in text:
            return QueryIntent.STANDARD_COMPARISON

        # Check for Amendment
        if "amendment" in text or "latest amendment" in text or "revised in" in text:
            return QueryIntent.AMENDMENT

        # Check for QCO / Mandatory orders
        if (
            "qco" in text
            or "quality control order" in text
            or "mandatory order" in text
            or "notified by ministry" in text
        ):
            return QueryIntent.QCO

        # Check for Certification / License / Scheme
        if (
            "certification" in text
            or "isi mark" in text
            or "license" in text
            or "licence" in text
            or "scheme" in text
            or "crs" in text
            or "fmcs" in text
            or "how to get certified" in text
        ):
            return QueryIntent.CERTIFICATION

        # Check for Compliance / Testing requirements
        if (
            "compliance" in text
            or "requirements" in text
            or "test method" in text
            or "proof pressure" in text
            or "leakage current" in text
            or "clause" in text
        ):
            return QueryIntent.COMPLIANCE

        # Check for Testing Laboratory
        if "lab" in text or "laboratory" in text or "testing center" in text:
            return QueryIntent.LABORATORY

        # Check for General Portal / Fee / Services
        if (
            "fees" in text
            or "portal" in text
            or "manak online" in text
            or "know your standard" in text
        ):
            return QueryIntent.GENERAL_BIS_SERVICE

        # Default fallback to Standard Lookup
        return QueryIntent.STANDARD_LOOKUP
