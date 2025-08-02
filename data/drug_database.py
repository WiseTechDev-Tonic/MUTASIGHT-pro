"""
Drug Database Initialization for MutaSight AI Platform
Contains real pharmaceutical drug data for research and development
"""

import json
from app import db
from models import DrugData

def initialize_drug_data():
    """Initialize the drug database with real pharmaceutical compounds"""
    
    # Check if data already exists
    if DrugData.query.first():
        return
    
    # Real pharmaceutical drug data
    drugs_data = [
        {
            "name": "Aspirin",
            "generic_name": "Acetylsalicylic Acid",
            "brand_names": json.dumps(["Bayer Aspirin", "Bufferin", "Ecotrin"]),
            "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
            "inchi": "InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)",
            "molecular_formula": "C9H8O4",
            "molecular_weight": 180.16,
            "therapeutic_class": "Analgesic/Anti-inflammatory",
            "mechanism_of_action": "Irreversibly inhibits cyclooxygenase-1 and -2 (COX-1 and COX-2) enzymes, which results in decreased formation of prostaglandin precursors.",
            "indications": "Pain relief, fever reduction, inflammation reduction, cardiovascular protection",
            "contraindications": "Hypersensitivity to salicylates, active peptic ulcer disease, bleeding disorders",
            "side_effects": "Gastrointestinal upset, bleeding, tinnitus, Reye's syndrome in children",
            "dosage_forms": json.dumps(["Tablet", "Enteric-coated tablet", "Chewable tablet"])
        },
        {
            "name": "Ibuprofen",
            "generic_name": "Ibuprofen",
            "brand_names": json.dumps(["Advil", "Motrin", "Nurofen"]),
            "smiles": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
            "inchi": "InChI=1S/C13H18O2/c1-9(2)8-11-4-6-12(7-5-11)10(3)13(14)15/h4-7,9-10H,8H2,1-3H3,(H,14,15)",
            "molecular_formula": "C13H18O2",
            "molecular_weight": 206.28,
            "therapeutic_class": "NSAID",
            "mechanism_of_action": "Reversibly inhibits cyclooxygenase-1 and -2 (COX-1 and COX-2) enzymes, which results in decreased formation of prostaglandin precursors.",
            "indications": "Pain relief, fever reduction, inflammation reduction",
            "contraindications": "Hypersensitivity to ibuprofen or other NSAIDs, active peptic ulcer disease",
            "side_effects": "Gastrointestinal upset, cardiovascular risks, kidney problems, dizziness",
            "dosage_forms": json.dumps(["Tablet", "Capsule", "Liquid gel", "Suspension"])
        },
        {
            "name": "Paracetamol",
            "generic_name": "Acetaminophen",
            "brand_names": json.dumps(["Tylenol", "Panadol", "Calpol"]),
            "smiles": "CC(=O)NC1=CC=C(C=C1)O",
            "inchi": "InChI=1S/C8H9NO2/c1-6(10)9-7-2-4-8(11)5-3-7/h2-5,11H,1H3,(H,9,10)",
            "molecular_formula": "C8H9NO2",
            "molecular_weight": 151.16,
            "therapeutic_class": "Analgesic/Antipyretic",
            "mechanism_of_action": "Inhibits prostaglandin synthesis in the central nervous system and peripherally blocks pain impulse generation.",
            "indications": "Pain relief, fever reduction",
            "contraindications": "Hypersensitivity to acetaminophen, severe hepatic impairment",
            "side_effects": "Hepatotoxicity (in overdose), rash, blood disorders (rare)",
            "dosage_forms": json.dumps(["Tablet", "Capsule", "Suspension", "Suppository"])
        },
        {
            "name": "Atorvastatin",
            "generic_name": "Atorvastatin Calcium",
            "brand_names": json.dumps(["Lipitor", "Torvast", "Atorlip"]),
            "smiles": "CC(C)C1=C(C(=C(N1CC[C@H](C[C@H](CC(=O)O)O)O)C2=CC=C(C=C2)F)C3=CC=CC=C3)C(=O)NC4=CC=CC=C4",
            "inchi": "InChI=1S/C33H35FN2O5/c1-21(2)31-30(33(41)35-25-11-7-4-8-12-25)29(23-9-5-3-6-10-23)32(22-13-15-24(34)16-14-22)36(31)18-17-26(37)19-27(38)20-28(39)40/h3-16,21,26-27,37-38H,17-20H2,1-2H3,(H,35,41)(H,39,40)/t26-,27-/m1/s1",
            "molecular_formula": "C33H35FN2O5",
            "molecular_weight": 558.64,
            "therapeutic_class": "HMG-CoA Reductase Inhibitor",
            "mechanism_of_action": "Inhibits 3-hydroxy-3-methylglutaryl-coenzyme A (HMG-CoA) reductase, the rate-limiting enzyme in cholesterol synthesis.",
            "indications": "Hypercholesterolemia, cardiovascular disease prevention",
            "contraindications": "Active liver disease, pregnancy, breastfeeding",
            "side_effects": "Muscle pain, liver enzyme elevation, digestive problems, memory problems",
            "dosage_forms": json.dumps(["Tablet", "Film-coated tablet"])
        },
        {
            "name": "Metformin",
            "generic_name": "Metformin Hydrochloride",
            "brand_names": json.dumps(["Glucophage", "Fortamet", "Riomet"]),
            "smiles": "CN(C)C(=N)NC(=N)N",
            "inchi": "InChI=1S/C4H11N5/c1-9(2)4(7)8-3(5)6/h1-2H3,(H5,5,6,7,8)",
            "molecular_formula": "C4H11N5",
            "molecular_weight": 129.16,
            "therapeutic_class": "Biguanide Antidiabetic",
            "mechanism_of_action": "Decreases hepatic glucose production, decreases intestinal absorption of glucose, and improves insulin sensitivity.",
            "indications": "Type 2 diabetes mellitus, polycystic ovary syndrome",
            "contraindications": "Renal impairment, metabolic acidosis, diabetic ketoacidosis",
            "side_effects": "Gastrointestinal upset, lactic acidosis (rare), vitamin B12 deficiency",
            "dosage_forms": json.dumps(["Tablet", "Extended-release tablet", "Solution"])
        },
        {
            "name": "Amlodipine",
            "generic_name": "Amlodipine Besylate",
            "brand_names": json.dumps(["Norvasc", "Istin", "Amvasc"]),
            "smiles": "CCOC(=O)C1=C(NC(=C(C1C2=CC=CC=C2Cl)C(=O)OC)C)N",
            "inchi": "InChI=1S/C20H25ClN2O5/c1-4-28-20(25)18-15(11-27-3)23-12(2)16(19(24)26-10-9-22)17(18)13-7-5-6-8-14(13)21/h5-8,17,23H,4,9-11,22H2,1-3H3",
            "molecular_formula": "C20H25ClN2O5",
            "molecular_weight": 408.88,
            "therapeutic_class": "Calcium Channel Blocker",
            "mechanism_of_action": "Inhibits calcium ion influx across cell membranes selectively, with a greater effect on vascular smooth muscle cells than on cardiac muscle cells.",
            "indications": "Hypertension, coronary artery disease, angina pectoris",
            "contraindications": "Hypersensitivity to dihydropyridines, severe aortic stenosis",
            "side_effects": "Peripheral edema, dizziness, flushing, palpitations",
            "dosage_forms": json.dumps(["Tablet", "Capsule"])
        },
        {
            "name": "Losartan",
            "generic_name": "Losartan Potassium",
            "brand_names": json.dumps(["Cozaar", "Hyzaar", "Losacar"]),
            "smiles": "CCCCC1=NC(=C(N1CC2=CC=C(C=C2)C3=CC=CC=C3C4=NNN=N4)CO)Cl",
            "inchi": "InChI=1S/C22H23ClN6O/c1-2-3-8-20-24-21(23)19(14-30)29(20)13-15-9-11-16(12-10-15)17-6-4-5-7-18(17)22-25-27-28-26-22/h4-7,9-12,30H,2-3,8,13-14H2,1H3,(H,25,26,27,28)",
            "molecular_formula": "C22H23ClN6O",
            "molecular_weight": 422.91,
            "therapeutic_class": "Angiotensin II Receptor Blocker",
            "mechanism_of_action": "Blocks the binding of angiotensin II to the AT1 receptor, preventing vasoconstriction and aldosterone secretion.",
            "indications": "Hypertension, diabetic nephropathy, heart failure",
            "contraindications": "Hypersensitivity to losartan, pregnancy",
            "side_effects": "Dizziness, hyperkalemia, cough, angioedema",
            "dosage_forms": json.dumps(["Tablet", "Film-coated tablet"])
        },
        {
            "name": "Omeprazole",
            "generic_name": "Omeprazole",
            "brand_names": json.dumps(["Prilosec", "Losec", "Omez"]),
            "smiles": "COC1=CC2=C(C=C1)N=C(N2)CS(=O)C3=NC4=C(N3)C=C(C=C4)OC",
            "inchi": "InChI=1S/C17H19N3O3S/c1-22-13-5-3-11-7-18-17(19-15(11)9-13)10-24(21)16-20-14-8-12(23-2)4-6-16/h3-9H,10H2,1-2H3,(H,18,19,20)",
            "molecular_formula": "C17H19N3O3S",
            "molecular_weight": 345.42,
            "therapeutic_class": "Proton Pump Inhibitor",
            "mechanism_of_action": "Inhibits the H+/K+ ATPase enzyme system (proton pump) in gastric parietal cells, reducing gastric acid secretion.",
            "indications": "Gastroesophageal reflux disease, peptic ulcer disease, Zollinger-Ellison syndrome",
            "contraindications": "Hypersensitivity to omeprazole or other proton pump inhibitors",
            "side_effects": "Headache, diarrhea, abdominal pain, vitamin B12 deficiency",
            "dosage_forms": json.dumps(["Capsule", "Tablet", "Injection"])
        },
        {
            "name": "Levothyroxine",
            "generic_name": "Levothyroxine Sodium",
            "brand_names": json.dumps(["Synthroid", "Levoxyl", "Euthyrox"]),
            "smiles": "NC(CC1=CC(I)=C(OC2=CC(I)=C(I)C=C2I)C(I)=C1)C(O)=O",
            "inchi": "InChI=1S/C15H11I4NO4/c16-8-4-7(5-11(19)24-14-3-6(15)2-9(17)12(14)20)1-10(18)13(8)21-25-26(22,23)15/h1-4H,5H2,(H2,19,21)(H,22,23)/t11-/m0/s1",
            "molecular_formula": "C15H11I4NO4",
            "molecular_weight": 776.87,
            "therapeutic_class": "Thyroid Hormone",
            "mechanism_of_action": "Replaces or supplements endogenous thyroid hormone T4, which regulates metabolism, growth, and development.",
            "indications": "Hypothyroidism, thyroid cancer suppression, goiter",
            "contraindications": "Untreated adrenal insufficiency, acute myocardial infarction, hyperthyroidism",
            "side_effects": "Cardiac arrhythmias, nervousness, insomnia, weight loss",
            "dosage_forms": json.dumps(["Tablet", "Capsule", "Injection"])
        },
        {
            "name": "Sertraline",
            "generic_name": "Sertraline Hydrochloride",
            "brand_names": json.dumps(["Zoloft", "Lustral", "Serlift"]),
            "smiles": "CN[C@H]1CCC2=C(C1)C=C(Cl)C=C2Cl",
            "inchi": "InChI=1S/C17H17Cl2N/c1-20-17-9-8-13-14(11-17)6-7-15(18)10-16(13)19/h6-7,10-11,17,20H,8-9H2,1H3/t17-/m1/s1",
            "molecular_formula": "C17H17Cl2N",
            "molecular_weight": 306.23,
            "therapeutic_class": "SSRI Antidepressant",
            "mechanism_of_action": "Selectively inhibits the reuptake of serotonin, increasing serotonin levels in the synaptic cleft.",
            "indications": "Major depressive disorder, panic disorder, obsessive-compulsive disorder, PTSD",
            "contraindications": "Concomitant use with MAOIs, hypersensitivity to sertraline",
            "side_effects": "Nausea, diarrhea, insomnia, dizziness, sexual dysfunction",
            "dosage_forms": json.dumps(["Tablet", "Oral concentrate"])
        },
        {
            "name": "Fluoxetine",
            "generic_name": "Fluoxetine Hydrochloride",
            "brand_names": json.dumps(["Prozac", "Sarafem", "Fontex"]),
            "smiles": "CNCCC(C1=CC=CC=C1)OC2=CC=C(C=C2)C(F)(F)F",
            "inchi": "InChI=1S/C17H18F3NO/c1-21-12-11-16(13-5-3-2-4-6-13)22-15-9-7-14(8-10-15)17(18,19)20/h2-10,16,21H,11-12H2,1H3",
            "molecular_formula": "C17H18F3NO",
            "molecular_weight": 309.33,
            "therapeutic_class": "SSRI Antidepressant",
            "mechanism_of_action": "Selectively inhibits the reuptake of serotonin, increasing serotonin levels in the synaptic cleft.",
            "indications": "Major depressive disorder, obsessive-compulsive disorder, bulimia nervosa, panic disorder",
            "contraindications": "Concomitant use with MAOIs or thioridazine, hypersensitivity to fluoxetine",
            "side_effects": "Nausea, headache, insomnia, nervousness, sexual dysfunction",
            "dosage_forms": json.dumps(["Capsule", "Tablet", "Solution"])
        },
        {
            "name": "Warfarin",
            "generic_name": "Warfarin Sodium",
            "brand_names": json.dumps(["Coumadin", "Jantoven", "Marevan"]),
            "smiles": "CC(=O)CC(C1=CC=CC=C1)C2=C(O)C3=CC=CC=C3OC2=O",
            "inchi": "InChI=1S/C19H16O4/c1-12(20)11-15(13-7-3-2-4-8-13)17-18(21)14-9-5-6-10-16(14)23-19(17)22/h2-10,15,21H,11H2,1H3",
            "molecular_formula": "C19H16O4",
            "molecular_weight": 308.33,
            "therapeutic_class": "Anticoagulant",
            "mechanism_of_action": "Inhibits vitamin K epoxide reductase, preventing the synthesis of vitamin K-dependent clotting factors.",
            "indications": "Thromboembolism prevention, atrial fibrillation, mechanical heart valves",
            "contraindications": "Active bleeding, pregnancy, severe liver disease",
            "side_effects": "Bleeding, bruising, hair loss, skin necrosis",
            "dosage_forms": json.dumps(["Tablet", "Injection"])
        },
        {
            "name": "Insulin Glargine",
            "generic_name": "Insulin Glargine",
            "brand_names": json.dumps(["Lantus", "Toujeo", "Basaglar"]),
            "smiles": "Complex protein structure - insulin analog",
            "inchi": "Complex protein structure",
            "molecular_formula": "C267H404N72O78S6",
            "molecular_weight": 6063.0,
            "therapeutic_class": "Long-acting Insulin",
            "mechanism_of_action": "Binds to insulin receptors, facilitating glucose uptake by cells and regulating glucose metabolism.",
            "indications": "Type 1 diabetes mellitus, Type 2 diabetes mellitus",
            "contraindications": "Hypoglycemia, hypersensitivity to insulin glargine",
            "side_effects": "Hypoglycemia, injection site reactions, weight gain, lipodystrophy",
            "dosage_forms": json.dumps(["Injection", "Pre-filled pen"])
        },
        {
            "name": "Hydrochlorothiazide",
            "generic_name": "Hydrochlorothiazide",
            "brand_names": json.dumps(["Microzide", "Aquazide", "HydroDIURIL"]),
            "smiles": "NS(=O)(=O)C1=CC2=C(C=C1Cl)NCNS2(=O)=O",
            "inchi": "InChI=1S/C7H8ClN3O4S2/c8-4-1-5-7(2-6(4)16(9,12)13)17(14,15)11-3-10-5/h1-2,10-11H,3H2,(H2,9,12,13)",
            "molecular_formula": "C7H8ClN3O4S2",
            "molecular_weight": 297.74,
            "therapeutic_class": "Thiazide Diuretic",
            "mechanism_of_action": "Inhibits sodium chloride reabsorption in the distal convoluted tubule of the nephron, increasing water and electrolyte excretion.",
            "indications": "Hypertension, edema, heart failure",
            "contraindications": "Anuria, hypersensitivity to thiazides or sulfonamides",
            "side_effects": "Hyponatremia, hypokalemia, hyperuricemia, glucose intolerance",
            "dosage_forms": json.dumps(["Tablet", "Capsule", "Solution"])
        },
        {
            "name": "Furosemide",
            "generic_name": "Furosemide",
            "brand_names": json.dumps(["Lasix", "Disal", "Frusol"]),
            "smiles": "NS(=O)(=O)C1=CC(=C(C=C1)NC2=CC=CC=C2C(=O)O)Cl",
            "inchi": "InChI=1S/C12H11ClN2O5S/c13-9-6-10(21(14,19)20)4-5-11(9)15-8-3-1-2-7(12(16)17)8/h1-6,15H,(H,16,17)(H2,14,19,20)",
            "molecular_formula": "C12H11ClN2O5S",
            "molecular_weight": 330.75,
            "therapeutic_class": "Loop Diuretic",
            "mechanism_of_action": "Inhibits sodium, chloride, and water reabsorption in the thick ascending limb of the loop of Henle.",
            "indications": "Edema, heart failure, hypertension, renal disease",
            "contraindications": "Anuria, hypersensitivity to furosemide",
            "side_effects": "Dehydration, electrolyte imbalance, ototoxicity, kidney damage",
            "dosage_forms": json.dumps(["Tablet", "Injection", "Solution"])
        }
    ]
    
    # Add drugs to database
    for drug_data in drugs_data:
        drug = DrugData(**drug_data)
        db.session.add(drug)
    
    try:
        db.session.commit()
        print(f"Successfully initialized drug database with {len(drugs_data)} drugs")
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing drug database: {e}")

if __name__ == "__main__":
    # For testing purposes
    from app import app
    with app.app_context():
        initialize_drug_data()
