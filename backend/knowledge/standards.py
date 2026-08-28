# Knowledge base definitions for Indian Standards
from typing import List, Dict, Any

SEED_STANDARDS: List[Dict[str, Any]] = [
    {
        "is_number": "IS 2347:2017",
        "title": "Domestic Pressure Cookers — Specification (Fifth Revision)",
        "year": 2017,
        "status": "Active",
        "scope": "Specifies requirements for domestic pressure cookers made of aluminum alloys or stainless steel having a nominal capacity not exceeding 10 liters.",
        "category": "Mechanical Engineering",
        "industry": "Cookware & Domestic Appliances",
        "committee": "MED 33 (Domestic and Commercial Gas Burning and Cookware Appliances)",
        "keywords": "pressure cooker, domestic cooker, stainless steel cooker, aluminium cooker, safety valve, gasket, burst pressure, cooking vessel, pressure cooking equipment",
        "publication_date": "2017-06-15",
        "effective_date": "2018-01-01",
        "source_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/is_details/2347",
        "is_demo": False,
        "clauses": [
            {
                "section": "4",
                "clause": "4.1",
                "page": 3,
                "title": "Material Requirements",
                "content": "Cooker body and lid shall be manufactured from stainless steel conforming to Grade 304 or food-grade aluminum alloy conforming to IS 21. Gaskets shall be made of food-grade synthetic or natural rubber conforming to IS 7466 without imparting odor or toxicity."
            },
            {
                "section": "5",
                "clause": "5.2",
                "page": 5,
                "title": "Safety Devices and Pressure Relief",
                "content": "Every cooker must be equipped with at least two independent pressure relief devices: a primary weight valve operating at nominal pressure (approx 100 kPa / 1.0 kgf/cm²) and a secondary safety valve or fusible plug operating between 130 kPa to 200 kPa before proof pressure is exceeded."
            },
            {
                "section": "6",
                "clause": "6.1",
                "page": 8,
                "title": "Operating Pressure Test",
                "content": "The cooker shall reach and maintain an operating pressure of 100 ± 10 kPa during normal cooking cycle without leakage around the rim or gasket."
            },
            {
                "section": "7",
                "clause": "7.3",
                "page": 11,
                "title": "Hydrostatic Proof Pressure Test",
                "content": "The assembled cooker body and lid shall withstand hydrostatic pressure equal to twice the nominal operating pressure (minimum 200 kPa) for 10 minutes without permanent deformation or leakage."
            },
            {
                "section": "8",
                "clause": "8.1",
                "page": 13,
                "title": "Bursting Pressure Test",
                "content": "When subjected to hydrostatic pressure, the cooker body and lid locking mechanism shall not fail or burst at pressures lower than 3 times the nominal operating pressure (minimum 300 kPa)."
            },
            {
                "section": "9",
                "clause": "9.1",
                "page": 15,
                "title": "Marking and Labelling",
                "content": "Each pressure cooker shall be legibly and indelibly marked with: Manufacturer's name or trademark, Nominal capacity in liters, Batch number or manufacturing date, Model designation, and the Standard Mark (ISI Mark) under licence from BIS."
            }
        ]
    },
    {
        "is_number": "IS 302-2-3:2021",
        "title": "Safety of Household and Similar Electrical Appliances — Particular Requirements for Electric Irons",
        "year": 2021,
        "status": "Active",
        "scope": "Covers safety requirements for electric dry irons and steam irons for household and similar use, rated voltage not exceeding 250V AC.",
        "category": "Electrotechnical",
        "industry": "Electrical Consumer Appliances",
        "committee": "ETD 32 (Electrical Appliances)",
        "keywords": "electric iron, steam iron, dry iron, electrical safety, thermostat, thermal cutout, soleplate",
        "publication_date": "2021-04-10",
        "effective_date": "2021-10-01",
        "source_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/is_details/302-2-3",
        "is_demo": False,
        "clauses": [
            {
                "section": "8",
                "clause": "8.1",
                "page": 4,
                "title": "Protection Against Access to Live Parts",
                "content": "Electric irons shall be constructed so that adequate protection against accidental contact with live parts is provided in all normal operating positions."
            },
            {
                "section": "13",
                "clause": "13.2",
                "page": 7,
                "title": "Leakage Current and Electric Strength at Operating Temperature",
                "content": "The leakage current shall not exceed 0.75 mA under working temperature, and the insulation shall withstand a high-voltage test of 1000V AC for 1 minute."
            },
            {
                "section": "19",
                "clause": "19.1",
                "page": 12,
                "title": "Abnormal Operation and Thermal Protection",
                "content": "Irons must incorporate a self-resetting thermostat and a non-self-resetting thermal cut-out that permanently interrupts power if the soleplate temperature exceeds 300°C due to thermostat failure."
            },
            {
                "section": "22",
                "clause": "22.3",
                "page": 16,
                "title": "Cord Guard and Flexibility Test",
                "content": "The supply cord entry shall have a resilient cord guard preventing sharp bends, tested for 20,000 flexing cycles without strand breakage."
            }
        ]
    },
    {
        "is_number": "IS 1293:2019",
        "title": "Plugs and Socket-Outlets of Rated Voltage up to and including 250 Volts and Rated Current up to and including 16 Amperes — Specification (Fourth Revision)",
        "year": 2019,
        "status": "Active",
        "scope": "Specifies requirements for domestic plugs and fixed or portable socket-outlets for AC only, with or without earthing contact, rated up to 250V and 16A.",
        "category": "Electrotechnical",
        "industry": "Electrical Wiring Accessories",
        "committee": "ETD 14 (Electrical Accessories)",
        "keywords": "plug, socket, outlet, 6A, 16A, round pin, electrical fitting, switchboard",
        "publication_date": "2019-07-20",
        "effective_date": "2020-06-01",
        "source_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/is_details/1293",
        "is_demo": False,
        "clauses": [
            {
                "section": "6",
                "clause": "6.1",
                "page": 5,
                "title": "Standard Ratings and Pin Configurations",
                "content": "Preferred ratings for domestic accessories are 6A 250V (2-pin or 3-pin) and 16A 250V (3-pin with solid brass earthing pin). Pin diameters and pitch must strictly match gauge dimensions in Table 1."
            },
            {
                "section": "10",
                "clause": "10.1",
                "page": 9,
                "title": "Protection Against Electric Shock and Shutter Mechanism",
                "content": "Socket outlets rated 6A and 16A shall be shuttered to prevent single-pin insertion of foreign metal objects or children's fingers."
            },
            {
                "section": "16",
                "clause": "16.1",
                "page": 14,
                "title": "Resistance to Heat, Fire, and Tracking",
                "content": "Molded insulating parts shall withstand glow-wire test at 850°C for parts in contact with current-carrying parts and 650°C for other external parts."
            }
        ]
    },
    {
        "is_number": "IS 694:2010",
        "title": "Polyvinyl Chloride Insulated Unsheathed and Sheathed Cables/Cords with Rigid and Flexible Conductor for Working Voltages up to and including 1100V",
        "year": 2010,
        "status": "Active",
        "scope": "Covers PVC insulated single-core and multi-core cables and cords for fixed wiring and flexible equipment cords rated up to 1100V.",
        "category": "Electrotechnical",
        "industry": "Cables & Conductors",
        "committee": "ETD 09 (Power Cables)",
        "keywords": "pvc cable, wire, copper conductor, aluminium conductor, 1100v, building wire, flexible cord",
        "publication_date": "2010-08-15",
        "effective_date": "2011-02-01",
        "source_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/is_details/694",
        "is_demo": False,
        "clauses": [
            {
                "section": "5",
                "clause": "5.1",
                "page": 3,
                "title": "Conductor Material and Resistance",
                "content": "Conductors shall consist of high conductivity annealed bare or tinned copper, or EC grade aluminum conforming to IS 8130 Class 1, Class 2, or Class 5 flexible conductors."
            },
            {
                "section": "6",
                "clause": "6.2",
                "page": 6,
                "title": "Insulation Thickness and Properties",
                "content": "The insulation shall be PVC Compound Type A or Type C (heat resistant) conforming to IS 5831, applied uniformly by extrusion without eccentricity exceeding 15%."
            },
            {
                "section": "16",
                "clause": "16.2",
                "page": 10,
                "title": "High Voltage AC Spark Test",
                "content": "Each drum length of cable shall withstand spark testing at 6 kV AC (for 1100V rating) during the extrusion line run without insulation breakdown."
            }
        ]
    },
    {
        "is_number": "IS 9873 (Part 1):2019",
        "title": "Safety of Toys — Part 1: Safety Aspects Related to Mechanical and Physical Properties",
        "year": 2019,
        "status": "Active",
        "scope": "Specifies requirements and methods of test for toys intended for use by children in all age groups below 14 years.",
        "category": "Consumer Products",
        "industry": "Toys & Children Goods",
        "committee": "PCD 24 (Toys Safety)",
        "keywords": "toys, child safety, small parts, choking hazard, sharp edges, mechanical physical properties",
        "publication_date": "2019-11-20",
        "effective_date": "2020-09-01",
        "source_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/is_details/9873-1",
        "is_demo": False,
        "clauses": [
            {
                "section": "4",
                "clause": "4.4",
                "page": 6,
                "title": "Small Parts and Choking Hazard for Children Under 36 Months",
                "content": "Toys intended for children under 3 years and removable components shall not completely fit into the small parts test cylinder of 31.7 mm diameter under specified drop or torque tests."
            },
            {
                "section": "4",
                "clause": "4.6",
                "page": 9,
                "title": "Edges, Points, and Wires",
                "content": "Accessible edges of metal or glass toys shall not present hazardous sharpness as evaluated by the sharpness tester under 6 N contact force."
            }
        ]
    },
    {
        "is_number": "IS 15652:2006",
        "title": "Insulating Mats for Electrical Purposes — Specification",
        "year": 2006,
        "status": "Active",
        "scope": "Specifies elastomeric insulating mats for use as floor covering for personal protection of workers around electrical switchboards up to 33 kV.",
        "category": "Electrotechnical",
        "industry": "Electrical Safety Equipment",
        "committee": "ETD 23 (High Voltage Switchgear)",
        "keywords": "insulating mat, electrical rubber mat, switchboard mat, dielectric mat, high voltage safety",
        "publication_date": "2006-05-10",
        "effective_date": "2006-11-01",
        "source_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/is_details/15652",
        "is_demo": False,
        "clauses": [
            {
                "section": "4",
                "clause": "4.1",
                "page": 2,
                "title": "Composition and Construction",
                "content": "Mats shall be made of synthetic elastomeric material, free from harmful metallic inserts, with an anti-skid ribbed or checkered upper surface."
            },
            {
                "section": "6",
                "clause": "6.1",
                "page": 4,
                "title": "Electrical Dielectric Breakdown Voltage",
                "content": "Class A mats (up to 3.3 kV) shall withstand 30 kV proof voltage; Class B (up to 11 kV) shall withstand 45 kV; Class C (up to 33 kV) shall withstand 65 kV breakdown test without puncture."
            }
        ]
    },
    {
        "is_number": "IS 14543:2018",
        "title": "Packaged Drinking Water (Other Than Packaged Natural Mineral Water) — Specification (Second Revision)",
        "year": 2018,
        "status": "Active",
        "scope": "Prescribes the requirements and methods of sampling and test for packaged drinking water other than packaged natural mineral water offered for direct human consumption in sealed containers.",
        "category": "Food and Agriculture",
        "industry": "Beverages & Water",
        "committee": "FAD 14 (Drinks and Drinking Water)",
        "keywords": "packaged drinking water, bottled water, drinking water, mineral water, microbiological safety, water jar, r/o water",
        "publication_date": "2018-03-15",
        "effective_date": "2019-01-01",
        "source_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/is_details/14543",
        "is_demo": False,
        "clauses": [
            {
                "section": "4",
                "clause": "4.1",
                "page": 3,
                "title": "Microbiological Requirements",
                "content": "Packaged drinking water shall be free from Escherichia coli, coliform bacteria, Faecal streptococci, Pseudomonas aeruginosa, and yeast and mould in 250 ml sample."
            },
            {
                "section": "5",
                "clause": "5.1",
                "page": 6,
                "title": "Packaging in Food Grade Containers",
                "content": "Water shall be packed in clean, hygienic, colorless, transparent and tamper-proof food grade plastic containers conforming to IS 15410 or glass containers conforming to IS 1388."
            },
            {
                "section": "8",
                "clause": "8.1",
                "page": 10,
                "title": "Mandatory ISI Marking and Labelling",
                "content": "Each container shall be legibly marked with: 'Packaged Drinking Water', Brand name, Net quantity, Batch number, Date of manufacture, Best before date, and the mandatory Standard Mark (ISI Mark) with CM/L licence number."
            }
        ]
    },
    {
        "is_number": "IS 2082:2018",
        "title": "Stationary Storage Type Electric Water Heaters for Domestic Use — Specification (Fifth Revision)",
        "year": 2018,
        "status": "Active",
        "scope": "Specifies safety and performance requirements for stationary storage type electric water heaters (geysers) intended for domestic and similar use, rated voltage not exceeding 250V AC.",
        "category": "Electrotechnical",
        "industry": "Electrical Consumer Appliances",
        "committee": "ETD 32 (Electrical Appliances)",
        "keywords": "electric water heater, storage water heater, geyser, instantaneous water heater, water heating appliance, IS 302, thermostat, pressure tank",
        "publication_date": "2018-05-20",
        "effective_date": "2019-01-01",
        "source_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/is_details/2082",
        "is_demo": False,
        "clauses": [
            {
                "section": "7",
                "clause": "7.1",
                "page": 4,
                "title": "Rated Capacity and Tank Pressure Rating",
                "content": "Water heaters shall be designed for closed (unvented) operation withstanding working hydrostatic pressure of minimum 0.6 MPa (6.0 bar) or as declared up to 0.8 MPa without tank rupture."
            },
            {
                "section": "13",
                "clause": "13.2",
                "page": 8,
                "title": "Insulation Resistance and High Voltage Test",
                "content": "The insulation resistance between live parts and the grounded metal water tank shall not be less than 50 Megohms, tested at 500V DC."
            },
            {
                "section": "19",
                "clause": "19.1",
                "page": 14,
                "title": "Thermal Safety and Non-Self-Resetting Cut-Out",
                "content": "Every storage water heater must incorporate an independent non-self-resetting thermal cut-out that positively disconnects both poles of the electrical supply if the water temperature reaches 95 ± 5°C."
            }
        ]
    }
]
