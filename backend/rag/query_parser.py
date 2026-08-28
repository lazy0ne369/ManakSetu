import re
from typing import Optional, Dict, Any, List
from backend.rag.schemas import ParsedQuery, UserRole, QueryIntent
from backend.ingestion.cleaner import clean_text


class QueryParser:
    def __init__(self):
        # Regex to detect IS standard references: e.g. IS 2347:2017, IS 1293, IS:302-2-3, IS 9873 (Part 1)
        self.is_regex = re.compile(
            r"\b(?:IS\s*|is\s*|IS:)(\d+(?:\s*\([^\)]+\))?(?:-\d+)*(?::\d{4})?)\b",
            re.IGNORECASE,
        )

        # Products lexicon with exact whole-word / phrase tokens
        self.product_keywords = {
            "pressure cooker": [
                "pressure cooker", "pressure cookers", "pressure cooking", "cooker", "cookers",
                "autoclave vessel", "pressure-cooking equipment", "pressure vessels used for cooking",
                "cook food under pressure", "pressure-cooking"
            ],
            "electric iron": [
                "electric iron", "electric irons", "electrical iron", "electrical irons",
                "steam iron", "steam irons", "dry iron", "ironing appliance"
            ],
            "plug and socket": [
                "plug", "plugs", "socket", "sockets", "socket-outlet", "socket-outlets",
                "wall outlet", "pin plug"
            ],
            "pvc cable": [
                "pvc cable", "pvc cables", "electric cable", "electric cables", "copper cable",
                "insulated wire", "flexible cord", "cables and wires", "pvc insulated cables", "cables"
            ],
            "toy": [
                "toy", "toys", "children toy", "children toys", "doll", "plaything"
            ],
            "insulating mat": [
                "insulating mat", "insulating mats", "electrical mat", "electrical mats",
                "rubber mat", "switchboard mat", "dielectric mat"
            ],
            "packaged water": [
                "packaged drinking water", "packaged water", "mineral water", "bottled water",
                "bottled drinking water", "drinking water"
            ],
            "electric water heater": [
                "electric water heater", "electric water heaters", "water heater", "water heaters",
                "geyser", "geysers", "storage water heater", "instantaneous water heater",
                "water heating appliance", "electric storage water heaters"
            ],
            "cement": ["cement", "opc", "portland cement"],
            "steel": ["steel bar", "steel bars", "tmt bar", "rebar", "reinforcement steel"],
        }

        # Materials lexicon
        self.material_keywords = {
            "stainless steel": ["stainless steel", "ss 304", "ss304", "steel"],
            "aluminum": ["aluminum", "aluminium", "hindalium"],
            "pvc": ["pvc", "polyvinyl chloride", "thermoplastic"],
            "copper": ["copper", "bare copper", "tinned copper"],
            "rubber": ["rubber", "elastomer", "synthetic rubber"],
            "brass": ["brass"],
        }

        # Industry vs Consumer indicators
        self.industry_keywords = [
            "manufacture", "manufacturer", "manufacturers", "manufacturing", "produce", "producer",
            "factory", "import", "importer", "export", "exporter", "industry",
            "sti", "compliance", "audit", "license", "licence", "testing lab", "batch"
        ]

        self.consumer_keywords = [
            "buy", "buying", "consumer", "customer", "purchase", "purchasing",
            "home", "kitchen", "safe", "safety", "verify mark", "isi logo", "fake"
        ]

    def parse(self, query: str, user_role_override: Optional[str] = None) -> ParsedQuery:
        clean_q = clean_text(query)
        lower_q = clean_q.lower()

        # 1. Check for explicit IS number
        is_number = None
        is_match = self.is_regex.search(clean_q)
        if is_match:
            is_raw = is_match.group(1).strip()
            is_number = f"IS {is_raw}"

        # 2. Extract Product (Using strict word-boundary matching)
        extracted_product = None
        for canonical_product, synonyms in self.product_keywords.items():
            for syn in synonyms:
                pattern = r"(?:\b|_)" + re.escape(syn) + r"(?:\b|_)"
                if re.search(pattern, lower_q):
                    extracted_product = canonical_product
                    break
            if extracted_product:
                break

        # 3. Extract Material
        extracted_material = None
        for canonical_material, synonyms in self.material_keywords.items():
            for syn in synonyms:
                if re.search(r"\b" + re.escape(syn) + r"\b", lower_q):
                    extracted_material = canonical_material
                    break
            if extracted_material:
                break

        # 4. Extract User Role
        role = UserRole.CONSUMER
        if user_role_override:
            if user_role_override.lower() == "industry":
                role = UserRole.INDUSTRY
            elif user_role_override.lower() == "auditor":
                role = UserRole.AUDITOR
        else:
            has_industry = any(re.search(r"\b" + re.escape(w) + r"\b", lower_q) for w in self.industry_keywords)
            if has_industry:
                role = UserRole.INDUSTRY

        # 5. Extract Constraints
        constraints = []
        if "mandatory" in lower_q or "compulsory" in lower_q:
            constraints.append("mandatory_check")
        if "qco" in lower_q or "order" in lower_q:
            constraints.append("qco_focus")
        if "amendment" in lower_q or "revised" in lower_q or "revision" in lower_q:
            constraints.append("amendment_focus")
        if "scheme" in lower_q or "isi mark" in lower_q or "crs" in lower_q:
            constraints.append("certification_scheme_focus")

        # 6. Ambiguity check: Query is completely underspecified
        needs_clarification = False
        clarification_question = None

        # Truly ambiguous IF NO product AND NO IS number
        if not is_number and not extracted_product:
            is_ambiguous_phrase = any(
                phrase in lower_q
                for phrase in [
                    "what bis certification do i need",
                    "which bis standard should i follow for my product",
                    "can you tell me whether my product requires bis certification",
                    "what certification do i need",
                    "what standard do i need",
                    "how do i apply for a license",
                    "how to get bis license",
                    "how to get isi mark",
                    "i manufacture a machine",
                    "my product is a metal container",
                    "i manufacture a product",
                    "tell me everything i need to know about bis compliance",
                ]
            )
            has_ambiguous_noun = any(re.search(r"\b" + re.escape(noun) + r"\b", lower_q) for noun in ["machine", "metal container", "my product", "a product"])

            # Exclude general conceptual questions from clarification prompt
            is_conceptual_query = any(
                cq in lower_q
                for cq in [
                    "what is bis certification",
                    "difference between an indian standard",
                    "what is a quality control order",
                    "what is a qco",
                    "how can a consumer verify",
                    "what information is normally needed",
                    "relationship between a qco",
                    "mandatory or voluntary",
                    "is bis certification mandatory for every product",
                    "supplier tells me that",
                    "why did you recommend this standard",
                    "for every important conclusion",
                    "separate your ai interpretation",
                    "is the standard you recommended still current",
                    "what changed between the original standard",
                    "which version of the standard",
                    "related or superseding standards",
                ]
            )

            if (is_ambiguous_phrase or has_ambiguous_noun) and not is_conceptual_query:
                needs_clarification = True
                clarification_question = (
                    "Could you please specify the exact product or Indian Standard number (e.g., domestic pressure cooker, electric iron, PVC cables, IS 2347) you are inquiring about?"
                )

        return ParsedQuery(
            original_query=clean_q,
            product=extracted_product,
            material=extracted_material,
            intended_use="domestic" if "domestic" in lower_q or "household" in lower_q else "industrial" if "industrial" in lower_q else None,
            industry=None,
            user_role=role,
            intent=QueryIntent.STANDARD_LOOKUP,
            is_number=is_number,
            constraints=constraints,
            needs_clarification=needs_clarification,
            clarification_question=clarification_question,
        )
