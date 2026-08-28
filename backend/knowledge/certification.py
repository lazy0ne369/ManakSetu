# Certification schemes knowledge base
from typing import List, Dict, Any

SEED_SCHEMES: List[Dict[str, Any]] = [
    {
        "scheme_id": "Scheme-I",
        "scheme_name": "Product Certification Scheme (Standard Mark / ISI Mark)",
        "description": "BIS operates a product certification scheme under Scheme-I of Schedule-II of the BIS (Conformity Assessment) Regulations, 2018. The presence of the ISI Mark ensures conformity to Indian Standards.",
        "applicable_products": "Domestic Pressure Cookers, Electric Irons, Plugs & Sockets, PVC Cables, Steel, Cement, Toys, Cylinders, Bottled Water",
        "requirements": "1. In-house testing laboratory with calibrated instruments.\n2. Qualified quality control personnel.\n3. Compliance with Scheme of Testing and Inspection (STI).\n4. Factory audit by BIS inspecting officer.\n5. Passing of factory samples and independent laboratory verification.",
        "testing_info": "Initial factory inspection + testing of production samples at BIS recognized laboratories. Periodic surveillance audits and market sample testing.",
        "fee_structure": "Application fee: Rs 1,000; Audit charges: Rs 7,000/man-day; Annual license fee: Rs 1,000 + Marking fee based on production volume.",
        "source_url": "https://www.bis.gov.in/product-certification/product-certification-scheme-overview/",
        "status": "Active",
        "is_demo": False,
    },
    {
        "scheme_id": "Scheme-II (CRS)",
        "scheme_name": "Compulsory Registration Scheme (CRS)",
        "description": "Self-declaration of conformity based on test reports from BIS recognized laboratories. Mainly applicable to IT, electronics, solar, and mobile products under orders issued by MeitY and MNRE.",
        "applicable_products": "Laptops, Mobile Phones, LED Lighting, Power Banks, Smart Watches, Servers, Solar Inverters",
        "requirements": "1. Testing of product model in BIS recognized lab.\n2. Submission of test report within 90 days of issuance.\n3. Undertaking by manufacturer for conformity.\n4. Registration grant by BIS without prior factory audit.",
        "testing_info": "Testing of sample at BIS recognized laboratory in India. Surveillance includes random market purchase and testing.",
        "fee_structure": "Application fee: Rs 1,000; Processing fee: Rs 50,000 per product category; Annual renewal fee: Rs 20,000.",
        "source_url": "https://www.crsbis.in/BIS/",
        "status": "Active",
        "is_demo": False,
    },
    {
        "scheme_id": "FMCS",
        "scheme_name": "Foreign Manufacturers Certification Scheme (FMCS)",
        "description": "Enables overseas manufacturers to obtain BIS ISI mark license for exporting goods to India complying with mandatory or voluntary Indian Standards.",
        "applicable_products": "All products under Scheme-I manufactured outside India.",
        "requirements": "1. Authorized Indian Representative (AIR) residing in India.\n2. In-house test facilities at foreign manufacturing plant.\n3. Factory inspection by BIS officer abroad.\n4. Performance bank guarantee.",
        "testing_info": "Foreign factory audit + testing in India.",
        "fee_structure": "Application fee: USD 1,000 + Inspection travel expenses + Marking fee.",
        "source_url": "https://www.bis.gov.in/foreign-manufacturers-certification-scheme-fmcs/",
        "status": "Active",
        "is_demo": False,
    },
    {
        "scheme_id": "Scheme-IV",
        "scheme_name": "Certificate of Conformity (CoC) / Lot Testing",
        "description": "Grant of certificate of conformity for a specific batch or lot of goods inspected and tested prior to dispatch.",
        "applicable_products": "Specific industrial supplies, bulk commodities, transformers, precision valves.",
        "requirements": "Drawing of samples from a specific manufactured lot and complete laboratory testing.",
        "testing_info": "Lot inspection and batch testing.",
        "fee_structure": "Lot inspection fee + Lab testing fees.",
        "source_url": "https://www.bis.gov.in/certificate-of-conformity/",
        "status": "Active",
        "is_demo": False,
    }
]
