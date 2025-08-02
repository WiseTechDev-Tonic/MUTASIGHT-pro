"""
Excipients Database Initialization for MutaSight AI Platform
Contains real pharmaceutical excipient data for formulation development
"""

import json
from app import db
from models import Excipient

def initialize_excipients_data():
    """Initialize the excipients database with real pharmaceutical excipients"""
    
    # Check if data already exists
    if Excipient.query.first():
        return
    
    # Real pharmaceutical excipient data
    excipients_data = [
        {
            "name": "Microcrystalline Cellulose",
            "chemical_name": "Cellulose, microcrystalline",
            "cas_number": "9004-34-6",
            "function": "binder",
            "description": "White, odorless, tasteless, crystalline powder composed of porous particles. Excellent binder and disintegrant properties.",
            "compatibility": json.dumps({
                "acids": "Compatible",
                "bases": "Compatible", 
                "oxidizing_agents": "Incompatible",
                "reducing_agents": "Compatible"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). LD50 > 5000 mg/kg (oral, rat)",
            "regulatory_status": "FDA approved",
            "typical_concentration": "5-20% w/w",
            "physical_properties": json.dumps({
                "appearance": "White powder",
                "particle_size": "50-100 μm",
                "moisture_content": "≤ 5.0%",
                "pH": "5.0-7.5",
                "bulk_density": "0.26-0.31 g/cm³"
            })
        },
        {
            "name": "Lactose Monohydrate",
            "chemical_name": "α-Lactose monohydrate",
            "cas_number": "64044-51-5",
            "function": "filler",
            "description": "White to off-white crystalline powder or white masses, odorless and slightly sweet taste. Widely used filler and binder.",
            "compatibility": json.dumps({
                "amines": "Incompatible - Maillard reaction",
                "amino_acids": "Incompatible - Maillard reaction",
                "acids": "Compatible",
                "bases": "Caution - may cause browning"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). Well tolerated except in lactose-intolerant individuals",
            "regulatory_status": "FDA approved",
            "typical_concentration": "10-80% w/w",
            "physical_properties": json.dumps({
                "appearance": "White crystalline powder",
                "solubility": "1 in 4.63 parts water",
                "melting_point": "201-202°C",
                "moisture_content": "≤ 0.5%",
                "pH": "4.0-6.5"
            })
        },
        {
            "name": "Magnesium Stearate",
            "chemical_name": "Octadecanoic acid, magnesium salt",
            "cas_number": "557-04-0",
            "function": "lubricant",
            "description": "Fine, white, precipitated or milled powder with a faint odor of stearic acid and a characteristic taste. Most commonly used lubricant.",
            "compatibility": json.dumps({
                "strong_acids": "Incompatible",
                "strong_bases": "Incompatible",
                "most_drugs": "Compatible",
                "ascorbic_acid": "May accelerate decomposition"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). LD50 > 10,000 mg/kg (oral, rat)",
            "regulatory_status": "FDA approved",
            "typical_concentration": "0.25-2.0% w/w",
            "physical_properties": json.dumps({
                "appearance": "Fine white powder",
                "melting_point": "117-150°C",
                "specific_surface_area": "1.5-2.5 m²/g",
                "loss_on_drying": "≤ 6.0%",
                "bulk_density": "0.159 g/cm³"
            })
        },
        {
            "name": "Croscarmellose Sodium",
            "chemical_name": "Cellulose, carboxymethyl ether, sodium salt, crosslinked",
            "cas_number": "74811-65-7",
            "function": "disintegrant",
            "description": "White, fibrous, free-flowing powder, practically odorless and tasteless. Excellent superdisintegrant properties.",
            "compatibility": json.dumps({
                "acids": "Stable",
                "bases": "Stable",
                "salts": "Compatible",
                "organic_solvents": "Insoluble"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). Non-toxic and non-irritating",
            "regulatory_status": "FDA approved",
            "typical_concentration": "0.5-5.0% w/w",
            "physical_properties": json.dumps({
                "appearance": "White fibrous powder",
                "pH": "6.0-8.0",
                "moisture_content": "≤ 10%",
                "particle_size": "< 50 μm",
                "swelling_capacity": "4-8 times"
            })
        },
        {
            "name": "Povidone",
            "chemical_name": "Poly(1-vinyl-2-pyrrolidinone)",
            "cas_number": "9003-39-8",
            "function": "binder",
            "description": "White to creamy white, odorless or practically odorless, hygroscopic powder. Excellent binder and film former.",
            "compatibility": json.dumps({
                "acids": "Compatible",
                "bases": "Compatible",
                "salts": "Compatible",
                "oxidizing_agents": "May be affected"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). LD50 > 100 g/kg (oral, rat)",
            "regulatory_status": "FDA approved",
            "typical_concentration": "0.5-5.0% w/w",
            "physical_properties": json.dumps({
                "appearance": "White hygroscopic powder",
                "molecular_weight": "Variable (K15-K120)",
                "glass_transition": "130-180°C",
                "solubility": "Freely soluble in water",
                "pH": "3.0-7.0"
            })
        },
        {
            "name": "Sodium Starch Glycolate",
            "chemical_name": "Starch, 2-(carboxymethyl) ether, sodium salt",
            "cas_number": "9063-38-1",
            "function": "disintegrant",
            "description": "White to off-white, odorless, tasteless, free-flowing powder. Excellent superdisintegrant with rapid uptake of water.",
            "compatibility": json.dumps({
                "divalent_cations": "May reduce disintegrant efficiency",
                "acids": "Compatible",
                "bases": "Compatible",
                "ascorbic_acid": "Compatible"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). Non-toxic and non-irritating",
            "regulatory_status": "FDA approved",
            "typical_concentration": "2-8% w/w",
            "physical_properties": json.dumps({
                "appearance": "White free-flowing powder",
                "pH": "6.5-8.0",
                "moisture_content": "≤ 10%",
                "particle_size": "30-100 μm",
                "swelling_index": "300-400%"
            })
        },
        {
            "name": "Hydroxypropyl Methylcellulose",
            "chemical_name": "Cellulose, 2-hydroxypropyl methyl ether",
            "cas_number": "9004-65-3",
            "function": "film_coating",
            "description": "White to slightly off-white, fibrous or granular powder. Excellent film-forming properties and controlled release matrix.",
            "compatibility": json.dumps({
                "acids": "Compatible",
                "bases": "Compatible",
                "salts": "Compatible",
                "organic_solvents": "Limited solubility"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). LD50 > 5000 mg/kg (oral, rat)",
            "regulatory_status": "FDA approved",
            "typical_concentration": "0.5-5.0% w/w (coating), 10-80% w/w (matrix)",
            "physical_properties": json.dumps({
                "appearance": "White fibrous powder",
                "viscosity": "Variable (3-100,000 mPa·s)",
                "gel_temperature": "50-55°C",
                "moisture_content": "≤ 5.0%",
                "pH": "5.5-8.0"
            })
        },
        {
            "name": "Colloidal Silicon Dioxide",
            "chemical_name": "Silicon dioxide, colloidal",
            "cas_number": "7631-86-9",
            "function": "glidant",
            "description": "Light, fine, white, amorphous, noncrystalline powder. Excellent glidant and anti-caking agent.",
            "compatibility": json.dumps({
                "most_excipients": "Compatible",
                "quaternary_ammonium": "May adsorb",
                "dibasic_calcium_phosphate": "Synergistic glidant effect"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). LD50 > 3160 mg/kg (oral, rat)",
            "regulatory_status": "FDA approved",
            "typical_concentration": "0.1-1.0% w/w",
            "physical_properties": json.dumps({
                "appearance": "Light white powder",
                "particle_size": "5-50 nm",
                "specific_surface_area": "175-225 m²/g",
                "loss_on_drying": "≤ 2.5%",
                "pH": "3.5-4.5"
            })
        },
        {
            "name": "Mannitol",
            "chemical_name": "D-Mannitol",
            "cas_number": "69-65-8",
            "function": "filler",
            "description": "White, odorless, crystalline powder or granules with a sweet taste. Non-hygroscopic sugar alcohol.",
            "compatibility": json.dumps({
                "amines": "Compatible",
                "acids": "Compatible",
                "bases": "Compatible",
                "reducing_sugars": "No Maillard reaction"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). LD50 13,500-20,000 mg/kg (oral, rat)",
            "regulatory_status": "FDA approved",
            "typical_concentration": "10-90% w/w",
            "physical_properties": json.dumps({
                "appearance": "White crystalline powder",
                "melting_point": "165-169°C",
                "solubility": "1 in 5.5 parts water",
                "hygroscopicity": "Non-hygroscopic",
                "compactability": "Good"
            })
        },
        {
            "name": "Stearic Acid",
            "chemical_name": "Octadecanoic acid",
            "cas_number": "57-11-4",
            "function": "lubricant",
            "description": "Hard, white or faintly yellowish, somewhat glossy, crystalline solid or white to yellowish-white powder.",
            "compatibility": json.dumps({
                "alkaline_substances": "Forms soaps",
                "metallic_oxides": "Forms metallic stearates",
                "most_drugs": "Compatible"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). LD50 > 20,000 mg/kg (oral, rat)",
            "regulatory_status": "FDA approved",
            "typical_concentration": "0.5-2.0% w/w",
            "physical_properties": json.dumps({
                "appearance": "White waxy solid",
                "melting_point": "67-72°C",
                "acid_value": "197-211",
                "iodine_value": "≤ 4.0",
                "moisture_content": "≤ 0.25%"
            })
        },
        {
            "name": "Talc",
            "chemical_name": "Magnesium silicate hydroxide",
            "cas_number": "14807-96-6",
            "function": "glidant",
            "description": "Very fine, white to grayish-white, odorless, impalpable, unctuous, crystalline powder. Excellent glidant and anti-adherent.",
            "compatibility": json.dumps({
                "most_excipients": "Compatible",
                "quaternary_ammonium": "May adsorb",
                "weak_bases": "Compatible"
            }),
            "toxicity_data": "Generally recognized as safe for pharmaceutical use. Avoid inhalation.",
            "regulatory_status": "FDA approved",
            "typical_concentration": "1-10% w/w",
            "physical_properties": json.dumps({
                "appearance": "White crystalline powder",
                "particle_size": "0.1-50 μm",
                "specific_surface_area": "2.5-7.5 m²/g",
                "loss_on_ignition": "≤ 7.0%",
                "pH": "7.0-10.0"
            })
        },
        {
            "name": "Crospovidone",
            "chemical_name": "Poly(1-vinyl-2-pyrrolidinone), crosslinked",
            "cas_number": "25249-54-1",
            "function": "disintegrant",
            "description": "White to creamy-white, odorless, practically tasteless, highly crosslinked polymer. Excellent superdisintegrant.",
            "compatibility": json.dumps({
                "acids": "Compatible",
                "bases": "Compatible",
                "salts": "Compatible",
                "organic_solvents": "Insoluble"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). Non-toxic and non-irritating",
            "regulatory_status": "FDA approved",
            "typical_concentration": "2-5% w/w",
            "physical_properties": json.dumps({
                "appearance": "White to cream powder",
                "particle_size": "50-180 μm",
                "moisture_content": "≤ 5.0%",
                "pH": "5.0-8.0",
                "swelling_ratio": "12:1"
            })
        },
        {
            "name": "Polyethylene Glycol 400",
            "chemical_name": "Polyethylene glycol 400",
            "cas_number": "25322-68-3",
            "function": "plasticizer",
            "description": "Clear, colorless or slightly yellow, viscous liquid; practically odorless. Excellent plasticizer and solubilizer.",
            "compatibility": json.dumps({
                "phenolic_compounds": "May form complexes",
                "tannins": "May form complexes",
                "most_drugs": "Compatible",
                "gelatin": "Plasticizing effect"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). LD50 26,400 mg/kg (oral, rat)",
            "regulatory_status": "FDA approved",
            "typical_concentration": "1-20% w/w",
            "physical_properties": json.dumps({
                "appearance": "Clear viscous liquid",
                "molecular_weight": "380-420",
                "viscosity": "105-130 mPa·s",
                "water_content": "≤ 0.5%",
                "pH": "4.5-7.5"
            })
        },
        {
            "name": "Sodium Lauryl Sulfate",
            "chemical_name": "Sodium dodecyl sulfate",
            "cas_number": "151-21-3",
            "function": "surfactant",
            "description": "White or cream to pale yellow crystals, flakes, or powder having a slight, characteristic odor. Anionic surfactant.",
            "compatibility": json.dumps({
                "cationic_surfactants": "Incompatible",
                "proteins": "May denature",
                "aluminum_salts": "Incompatible",
                "polyvalent_metal_salts": "Incompatible"
            }),
            "toxicity_data": "LD50 1,288 mg/kg (oral, rat). May cause irritation at high concentrations",
            "regulatory_status": "FDA approved",
            "typical_concentration": "0.5-2.0% w/w",
            "physical_properties": json.dumps({
                "appearance": "White crystalline powder",
                "melting_point": "204-207°C",
                "CMC": "8.1-8.4 mM",
                "HLB_value": "40",
                "solubility": "1 in 10 parts water"
            })
        },
        {
            "name": "Calcium Phosphate Dibasic",
            "chemical_name": "Dicalcium phosphate dihydrate",
            "cas_number": "7789-77-7",
            "function": "filler",
            "description": "White, odorless, tasteless powder or crystalline solid. Excellent directly compressible filler with good flow properties.",
            "compatibility": json.dumps({
                "tetracyclines": "Incompatible - chelation",
                "fluoroquinolones": "Incompatible - chelation",
                "iron_salts": "Incompatible - chelation",
                "most_other_drugs": "Compatible"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). Well tolerated dietary supplement",
            "regulatory_status": "FDA approved",
            "typical_concentration": "20-80% w/w",
            "physical_properties": json.dumps({
                "appearance": "White crystalline powder",
                "solubility": "Slightly soluble in water",
                "moisture_content": "≤ 1.0%",
                "bulk_density": "0.8-1.0 g/cm³",
                "pH": "7.0-8.5"
            })
        },
        {
            "name": "Gelatin",
            "chemical_name": "Gelatin",
            "cas_number": "9000-70-8",
            "function": "capsule_shell",
            "description": "Yellowish-white to faintly yellow-colored, nearly transparent, brittle sheets, shreds, or coarse powder. Used for capsule shells.",
            "compatibility": json.dumps({
                "aldehydes": "Cross-linking occurs",
                "tannins": "Precipitation may occur",
                "heavy_metal_salts": "Precipitation may occur",
                "strong_acids": "Hydrolysis may occur"
            }),
            "toxicity_data": "Generally recognized as safe (GRAS). Well tolerated food ingredient",
            "regulatory_status": "FDA approved",
            "typical_concentration": "20-100% w/w (capsule shell)",
            "physical_properties": json.dumps({
                "appearance": "Yellowish sheets or powder",
                "gel_strength": "150-300 Bloom",
                "moisture_content": "≤ 15%",
                "ash_content": "≤ 2.0%",
                "pH": "3.8-6.0"
            })
        }
    ]
    
    # Add excipients to database
    for excipient_data in excipients_data:
        excipient = Excipient(**excipient_data)
        db.session.add(excipient)
    
    try:
        db.session.commit()
        print(f"Successfully initialized excipients database with {len(excipients_data)} excipients")
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing excipients database: {e}")

if __name__ == "__main__":
    # For testing purposes
    from app import app
    with app.app_context():
        initialize_excipients_data()
