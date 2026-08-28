"""Authoritative General BIS Knowledge Base."""
from typing import Dict, Any, Optional

GENERAL_BIS_KNOWLEDGE_TOPICS: Dict[str, Dict[str, Any]] = {
    "what_is_bis_certification": {
        "title": "BIS Certification Overview & Statutory Requirement in India",
        "keywords": ["what is bis certification", "when is it required", "bis certification required"],
        "answer": (
            "**Bureau of Indian Standards (BIS) Certification** is India's national product conformity assessment system established under the **BIS Act, 2016**.\n\n"
            "### 1. When is BIS Certification Required?\n"
            "- **Mandatory Products (Under QCOs)**: The Government of India issues **Quality Control Orders (QCOs)** under Section 16 of the BIS Act, 2016. Any product listed under a notified QCO **must mandatorily obtain BIS certification** before manufacturing, importing, selling, or storing in India.\n"
            "- **Voluntary Products**: For products without an active QCO, BIS certification is **voluntary**, allowing manufacturers to obtain the ISI mark as a quality and safety differentiator.\n\n"
            "### 2. Primary Certification Routes\n"
            "- **Scheme-I (ISI Mark)**: Requires in-house laboratory testing, factory audit, and grant of a CM/L (Certification Marks Licence) number.\n"
            "- **Scheme-II (CRS - Compulsory Registration)**: Self-declaration of conformity based on test reports from BIS-recognized labs for IT & electronics."
        ),
        "key_points": [
            "Mandatory under statutory Quality Control Orders (QCOs) issued by line ministries (DPIIT, MeitY, Ministry of Power).",
            "Voluntary for other product categories unless notified in the official Gazette of India.",
            "Prohibits manufacturing, import, distribution, or sale of uncertified goods covered by a QCO under penalty of law.",
        ],
        "compliance_steps": [
            "1. Identify the applicable Indian Standard (IS) for your product.",
            "2. Check if a mandatory Quality Control Order (QCO) is enforced.",
            "3. Set up in-house testing facilities adhering to the Scheme of Testing & Inspection (STI).",
            "4. Submit online application on www.manakonline.in with requisite documentation and fees.",
            "5. Undergo factory audit and sample verification by BIS officers.",
        ],
    },
    "is_vs_scheme": {
        "title": "Difference Between an Indian Standard (IS) and a BIS Certification Scheme",
        "keywords": ["difference between an indian standard", "is vs certification scheme", "difference between is and bis scheme"],
        "answer": (
            "There is a fundamental regulatory distinction between an **Indian Standard (IS)** and a **BIS Certification Scheme**:\n\n"
            "| Aspect | Indian Standard (IS) | BIS Certification Scheme |\n"
            "| :--- | :--- | :--- |\n"
            "| **Definition** | A published technical specification defining product requirements, test methods, dimensions, and safety limits. | A legal and procedural framework under which BIS grants licenses to use the Standard Mark. |\n"
            "| **Authority** | Formulated by BIS Technical Sectional Committees (e.g. MED, ETD, CHD). | Prescribed by the Central Government under BIS (Conformity Assessment) Regulations, 2018. |\n"
            "| **Example** | **IS 2347:2017** (Specification for Domestic Pressure Cookers). | **Scheme-I (Product Certification)** or **Scheme-II (CRS)**. |\n"
            "| **Usage** | Anyone can read and manufacture according to an IS document. | Merely following the standard does NOT grant the right to use the ISI mark; a formal license (CM/L) under the Scheme is mandatory. |"
        ),
        "key_points": [
            "An Indian Standard (IS) is the technical benchmark document.",
            "A Certification Scheme is the legal conformity assessment process that authorizes the ISI / Standard Mark.",
            "Compliance with an Indian Standard without a BIS licence does NOT permit the use of the ISI mark.",
        ],
        "compliance_steps": [
            "1. Procure and comply with the technical specification in the relevant Indian Standard.",
            "2. Select the applicable conformity assessment scheme (Scheme-I, Scheme-II CRS, or FMCS).",
            "3. Apply on Manakonline for grant of licence (CM/L) before marking products with the ISI logo.",
        ],
    },
    "what_is_qco": {
        "title": "Quality Control Orders (QCO) & Impact on Manufacturers",
        "keywords": ["what is a quality control order", "what is a qco", "qco affect manufacturers", "how does a qco affect"],
        "answer": (
            "A **Quality Control Order (QCO)** is a statutory notification issued by the Central Government of India (via line ministries such as DPIIT, Ministry of Steel, MeitY, MoCA) under **Section 16 of the BIS Act, 2016**.\n\n"
            "### Legal Effect on Manufacturers & Importers:\n"
            "1. **Compulsory Standard Mark**: Products covered under a QCO must mandatorily conform to the specified Indian Standard and carry the **Standard Mark (ISI Mark or CRS Mark)** under a valid BIS licence.\n"
            "2. **Prohibition of Sale & Import**: No person shall manufacture, import, distribute, sell, lease, or exhibit for sale any goods covered by a QCO without a valid BIS license.\n"
            "3. **Penalties**: Violations attract severe penalties under Section 29 of the BIS Act, 2016, including imprisonment up to 2 years, hefty fines, and confiscation of non-compliant goods."
        ),
        "key_points": [
            "Issued by Central Line Ministries under Section 16 of the BIS Act, 2016 in public interest, safety, and national security.",
            "Makes Indian Standards legally binding on domestic manufacturers and foreign exporters.",
            "Strict penalties and seizure of uncertified stock under Section 29 of the BIS Act.",
        ],
        "compliance_steps": [
            "1. Review the Gazette notification to identify the enforcement date and target Indian Standard.",
            "2. Ensure factory manufacturing processes and in-house laboratory satisfy standard requirements.",
            "3. Apply for BIS certification well before the enforcement deadline to avoid production halts.",
        ],
    },
    "consumer_verification": {
        "title": "Consumer Verification of BIS Certified Products",
        "keywords": ["how can a consumer verify", "how to check if a product is bis certified", "verify whether a product is bis certified", "check bis certification"],
        "answer": (
            "Consumers can verify the authenticity of BIS certification using the following methods:\n\n"
            "### 1. Inspect the ISI Mark on Packaging\n"
            "- An authentic ISI mark consists of the **ISI logo**, the **Indian Standard number (e.g. IS 2347)** on top, and a **7-digit or 8-digit CM/L (Certification Marks Licence) number** at the bottom: `CM/L-XXXXXXX`.\n\n"
            "### 2. Verify via BIS CARE Mobile App\n"
            "- Download the official **BIS CARE App** (Android / iOS).\n"
            "- Use the **'Verify License Details'** feature and enter the CM/L number.\n"
            "- The app will display the manufacturer's name, brand, product scope, factory address, and licence validity status.\n\n"
            "### 3. Electronic Products (CRS Registration)\n"
            "- For laptops, mobile phones, and adapters under Scheme-II (CRS), look for the standard CRS mark with the **Registration Number: R-XXXXXXXX** and web URL `www.crsbis.in`."
        ),
        "key_points": [
            "Authentic ISI mark always includes IS Number on top and CM/L licence number below.",
            "Verify real-time licence validity using the free BIS CARE App.",
            "CRS electronic goods must show the registration number (R-number) and CRS portal link.",
        ],
        "compliance_steps": [
            "1. Locate the ISI or CRS mark on the product rating plate and packaging.",
            "2. Read the 7-digit CM/L number or R-number.",
            "3. Enter the number into the 'Verify License Details' section of the BIS CARE App.",
            "4. File a complaint via BIS CARE App if counterfeit or expired marks are detected.",
        ],
    },
    "standard_determination_info": {
        "title": "Information Required to Determine Standard Applicability",
        "keywords": ["what information is normally needed", "information needed to determine which bis standard", "determine which bis standard applies"],
        "answer": (
            "To accurately determine which Indian Standard (IS) applies to a product, the following technical details are required:\n\n"
            "1. **Generic Product Name & Intended Use**: (e.g. Domestic pressure cooker, Industrial PVC cable, Electric dry iron).\n"
            "2. **Material Composition**: (e.g. Stainless steel, Aluminum alloy, Copper conductor, Polyvinyl chloride).\n"
            "3. **Operating Parameters & Ratings**: (e.g. Rated voltage up to 1100V, nominal capacity in liters, wattage, operating pressure).\n"
            "4. **User Environment**: (e.g. Domestic / household vs Commercial / industrial / hazardous area).\n"
            "5. **Product Sub-Category & Configurations**: (e.g. Instantaneous vs Storage water heater, 6A vs 16A plug/socket)."
        ),
        "key_points": [
            "Product name and specific intended application.",
            "Material of construction (metals, plastics, insulation).",
            "Technical capacity, voltage, wattage, or pressure ratings.",
            "Domestic vs industrial operating environment.",
        ],
        "compliance_steps": [
            "1. Compile complete technical specifications and user manual.",
            "2. Search the BIS Product Manual and e-BIS directory for matching scopes.",
            "3. Confirm whether any specialized component standards apply simultaneously.",
        ],
    },
    "qco_relationship": {
        "title": "Relationship Between QCO, Indian Standard, and BIS Certification",
        "keywords": ["relationship between a qco, an indian standard", "relationship between a qco and indian standard", "relationship between qco"],
        "answer": (
            "The relationship operates as a 3-pillar regulatory hierarchy:\n\n"
            "1. **Indian Standard (IS)** = *The Technical Benchmark*: Formulated by expert technical committees specifying quality, safety, and testing requirements.\n"
            "2. **Quality Control Order (QCO)** = *The Legal Mandate*: Issued by the Central Government under Section 16 of the BIS Act, 2016, making the Indian Standard mandatory by law.\n"
            "3. **BIS Certification (Licence)** = *The Operational Authorization*: The formal licence (CM/L under Scheme-I or R-number under Scheme-II) granted by BIS authorizing the manufacturer to apply the Standard Mark after passing audits and laboratory testing."
        ),
        "key_points": [
            "Indian Standard = What technical parameters the product must meet.",
            "QCO = Legal mandate making compliance compulsory.",
            "BIS Certification = Permission to apply the ISI mark upon audit and test verification.",
        ],
        "compliance_steps": [
            "1. Standard formulation by BIS committees.",
            "2. Notification of mandatory QCO by line ministry in Gazette of India.",
            "3. Manufacturer obtains CM/L licence from BIS to manufacture and sell legally.",
        ],
    },
    "mandatory_vs_voluntary": {
        "title": "Determining Mandatory vs Voluntary BIS Certification",
        "keywords": ["mandatory or voluntary", "whether certification is mandatory", "is bis certification mandatory for every product"],
        "answer": (
            "By default under the BIS Act, 2016, Indian Standards are **voluntary** unless explicitly brought under a statutory mandate:\n\n"
            "### How to Determine if Certification is Mandatory:\n"
            "1. **Check Central Government QCO Notifications**: If a line ministry (DPIIT, MoCA, Ministry of Steel, MeitY, MOP) has gazetted a Quality Control Order for the product, certification is **100% Mandatory**.\n"
            "2. **Check Compulsory Registration Scheme (CRS) List**: Electronic and IT goods notified under CRO by MeitY or MNRE require mandatory registration.\n"
            "3. **Sectoral Regulators**: Certain products (e.g. infant food, packaged drinking water, cement, structural steel) are mandated by sectoral regulations (FSSAI, Building Codes, CEA).\n"
            "4. **All Other Products**: Certification is **Voluntary**, allowing manufacturers to choose whether to apply for the ISI mark as a market advantage."
        ),
        "key_points": [
            "Indian Standards are voluntary by default.",
            "Standards become mandatory only when notified under a statutory QCO in the Gazette of India.",
            "Selling uncertified goods under an enforced QCO is illegal under Section 29 of the BIS Act.",
        ],
        "compliance_steps": [
            "1. Search the official BIS QCO repository at https://www.services.bis.gov.in/.",
            "2. Check DPIIT and relevant ministry gazette notifications.",
            "3. If listed, apply for mandatory Scheme-I/II certification prior to commercial launch.",
        ],
    },
    "supplier_misconception": {
        "title": "Supplier Claim Assessment: Is Following an Indian Standard Automatically Optional?",
        "keywords": ["supplier tells me that because our product follows an indian standard", "follows an indian standard, bis certification is automatically optional", "following the standard automatically allow me to use"],
        "answer": (
            "**The supplier's statement is incorrect and legally dangerous:**\n\n"
            "### Why the Claim is False:\n"
            "1. **QCO Mandate Overrides Voluntary Status**: If the product is covered under an active Quality Control Order (QCO) issued by the Government of India (e.g. pressure cookers, cables, electric irons, toys), compliance and certification are **strictly mandatory by law**.\n"
            "2. **No Automatic Right to the Standard Mark**: Merely manufacturing a product that complies with an Indian Standard does **NOT** grant legal permission to use the ISI mark or sell goods under a QCO. Using the ISI mark without a valid BIS Certification Marks Licence (CM/L) is a punishable criminal offense under Section 17 & 29 of the BIS Act, 2016.\n\n"
            "### What Must Be Verified:\n"
            "- Verify whether the product is covered by a gazetted QCO.\n"
            "- Ensure the factory holds a valid, active CM/L licence granted by BIS after official audit and sample testing."
        ),
        "key_points": [
            "Manufacturing to an Indian Standard does not confer permission to use the ISI mark without a BIS licence.",
            "If a QCO is in force, certification is legally compulsory under penalty of imprisonment and fines.",
            "Always verify active CM/L licence status on the BIS CARE App.",
        ],
        "compliance_steps": [
            "1. Check if product is covered under an active QCO.",
            "2. Apply for formal BIS licensing under Scheme-I / Scheme-II.",
            "3. Obtain valid CM/L before applying the ISI mark on goods.",
        ],
    },
    "versioning_and_amendments": {
        "title": "Indian Standard Versioning, Amendments & Currentness Rules",
        "keywords": ["is the standard you recommended still current", "what changed between the original standard and its latest amendment", "which version of the standard should a manufacturer rely on", "related or superseding standards"],
        "answer": (
            "Under BIS standardization rules:\n\n"
            "### 1. Which Version Governs Current Compliance?\n"
            "- Manufacturers must always comply with the **latest active revision of the Indian Standard along with all notified amendments**.\n"
            "- When a new revision is published, BIS typically grants a **transition period** (usually 6 to 12 months) during which both revisions may be recognized, after which the older revision is officially superseded.\n\n"
            "### 2. Role of Amendments\n"
            "- Amendments update specific clauses, test limits, or material grades without reissuing the entire standard. All amendments issued up to date are integral parts of the standard.\n\n"
            "### 3. Component & Cross-Referenced Standards\n"
            "- Primary product standards normative-reference complementary material and component standards (e.g. IS 21 for wrought aluminum, IS 7466 for rubber gaskets, IS 694 for supply cords)."
        ),
        "key_points": [
            "The active revision along with all notified amendments is legally binding.",
            "BIS publishes transition timelines on www.services.bis.gov.in when standards are revised.",
            "Normative component standards must also be satisfied for full product compliance.",
        ],
        "compliance_steps": [
            "1. Verify the current revision year and latest amendment numbers on the e-BIS portal.",
            "2. Update factory STI testing routines to reflect recent amendment changes.",
            "3. Procure raw materials from BIS-certified component suppliers where mandated.",
        ],
    },
    "evidence_first_principles": {
        "title": "Authoritative Evidence & Standard Provenance Hierarchy",
        "keywords": [
            "why did you recommend this standard", "show the specific evidence", "for every important conclusion",
            "separate your ai interpretation", "which part of the source document supports your claim that certification is mandatory",
            "which clause in the retrieved standard", "tell me the document title and page"
        ],
        "answer": (
            "Every regulatory recommendation by ManakSetu is grounded strictly in a 3-tier hierarchy of authoritative legal and technical evidence:\n\n"
            "1. **Statutory Quality Control Orders (QCOs)**: Published in the Gazette of India under Section 16 of the BIS Act, 2016 by Central Line Ministries (e.g. DPIIT, Ministry of Power, MoCA), establishing mandatory legal applicability.\n"
            "2. **Authoritative Indian Standards (IS)**: Technical specifications formulated by BIS Sectional Committees, providing normative clause requirements, proof limits, and test methods.\n"
            "3. **Scheme of Testing & Inspection (STI)**: Prescribed quality control sampling procedures and factory audit criteria for grant of license (CM/L).\n\n"
            "All cited clauses and document pages reflect verified excerpts from official Bureau of Indian Standards documentation."
        ),
        "key_points": [
            "Mandatory status derives directly from Gazette QCOs published under Section 16 of the BIS Act, 2016.",
            "Clause numbers (e.g. Cl. 4.1, 5.2, 7.3) specify verifiable test thresholds and material grades.",
            "Citations include document titles, clause identifiers, and official BIS verification links.",
        ],
        "compliance_steps": [
            "1. Cross-reference clause citations against the official standard document.",
            "2. Verify QCO gazette notifications on DPIIT / line ministry portals.",
            "3. Access the full text of Indian Standards on the BIS Standards Portal (manakonline.in).",
        ],
    },
}


def find_general_knowledge(query: str) -> Optional[Dict[str, Any]]:
    """Match a user query against general BIS knowledge topics."""
    lower_q = query.lower().strip()
    
    for topic_key, data in GENERAL_BIS_KNOWLEDGE_TOPICS.items():
        if any(kw in lower_q for kw in data["keywords"]):
            return data
            
    return None
