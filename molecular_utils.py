import re
import json
from typing import Dict, Any, Optional
import logging

class MolecularAnalyzer:
    """Simple molecular analysis without external chemistry libraries"""
    
    def __init__(self):
        # Atomic weights (simplified list)
        self.atomic_weights = {
            'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998,
            'P': 30.974, 'S': 32.065, 'Cl': 35.453, 'Br': 79.904, 'I': 126.904,
            'Na': 22.990, 'K': 39.098, 'Mg': 24.305, 'Ca': 40.078, 'Fe': 55.845,
            'Zn': 65.409, 'Cu': 63.546, 'Mn': 54.938, 'Co': 58.933, 'Ni': 58.693
        }
    
    def calculate_molecular_weight_from_formula(self, formula: str) -> float:
        """Calculate molecular weight from molecular formula"""
        try:
            # Parse molecular formula using regex
            pattern = r'([A-Z][a-z]?)(\d*)'
            matches = re.findall(pattern, formula)
            
            total_weight = 0.0
            for element, count in matches:
                count = int(count) if count else 1
                if element in self.atomic_weights:
                    total_weight += self.atomic_weights[element] * count
                else:
                    logging.warning(f"Unknown element: {element}")
            
            return round(total_weight, 2)
        except Exception as e:
            logging.error(f"Error calculating molecular weight: {e}")
            return 0.0
    
    def parse_smiles_basic(self, smiles: str) -> Dict[str, Any]:
        """Basic SMILES parsing to extract some information"""
        try:
            # Count atoms (very basic approach)
            atom_counts = {}
            
            # Remove brackets and bonds for simple counting
            simplified = re.sub(r'[\(\)\[\]=\-#@+\\/]', '', smiles)
            simplified = re.sub(r'[0-9]', '', simplified)  # Remove ring numbers
            
            # Count uppercase letters (atoms)
            i = 0
            while i < len(simplified):
                if simplified[i].isupper():
                    atom = simplified[i]
                    # Check for two-letter elements
                    if i + 1 < len(simplified) and simplified[i + 1].islower():
                        atom += simplified[i + 1]
                        i += 1
                    
                    atom_counts[atom] = atom_counts.get(atom, 0) + 1
                i += 1
            
            # Generate molecular formula
            molecular_formula = ''
            for atom in sorted(atom_counts.keys()):
                count = atom_counts[atom]
                if count == 1:
                    molecular_formula += atom
                else:
                    molecular_formula += f"{atom}{count}"
            
            # Calculate molecular weight
            molecular_weight = 0.0
            for atom, count in atom_counts.items():
                if atom in self.atomic_weights:
                    molecular_weight += self.atomic_weights[atom] * count
            
            return {
                'atom_counts': atom_counts,
                'molecular_formula': molecular_formula,
                'molecular_weight': round(molecular_weight, 2),
                'atom_count': sum(atom_counts.values())
            }
        
        except Exception as e:
            logging.error(f"Error parsing SMILES: {e}")
            return {}
    
    def estimate_properties(self, smiles: str) -> Dict[str, Any]:
        """Estimate basic molecular properties"""
        properties = {}
        
        try:
            # Count specific functional groups (basic patterns)
            properties['aromatic_rings'] = len(re.findall(r'c1c+c+c+c+c+1|C1=CC=CC=C1', smiles))
            properties['hydroxyl_groups'] = smiles.count('O') + smiles.count('OH')
            properties['nitrogen_count'] = smiles.count('N')
            properties['sulfur_count'] = smiles.count('S')
            properties['halogen_count'] = smiles.count('F') + smiles.count('Cl') + smiles.count('Br') + smiles.count('I')
            
            # Estimate lipophilicity (very rough)
            carbon_count = smiles.count('C') + smiles.count('c')
            oxygen_count = smiles.count('O')
            
            if oxygen_count > 0:
                properties['estimated_logp'] = round((carbon_count - oxygen_count) * 0.5, 2)
            else:
                properties['estimated_logp'] = round(carbon_count * 0.5, 2)
            
            # Basic drug-likeness assessment
            molecular_data = self.parse_smiles_basic(smiles)
            mw = molecular_data.get('molecular_weight', 0)
            
            properties['lipinski_violations'] = 0
            if mw > 500:
                properties['lipinski_violations'] += 1
            if properties['estimated_logp'] > 5:
                properties['lipinski_violations'] += 1
            if properties['hydroxyl_groups'] > 5:
                properties['lipinski_violations'] += 1
            if properties['nitrogen_count'] + properties['hydroxyl_groups'] > 10:
                properties['lipinski_violations'] += 1
            
            properties['drug_like'] = properties['lipinski_violations'] <= 1
            
        except Exception as e:
            logging.error(f"Error estimating properties: {e}")
        
        return properties

def analyze_molecule(input_value: str, input_type: str = 'smiles') -> Dict[str, Any]:
    """Main function to analyze a molecule"""
    analyzer = MolecularAnalyzer()
    results = {
        'input_value': input_value,
        'input_type': input_type,
        'success': True
    }
    
    try:
        if input_type.lower() == 'smiles':
            # Parse SMILES
            molecular_data = analyzer.parse_smiles_basic(input_value)
            properties = analyzer.estimate_properties(input_value)
            
            results.update(molecular_data)
            results.update(properties)
            results['smiles'] = input_value
            
        elif input_type.lower() == 'inchi':
            # Basic InChI handling (extract molecular formula if possible)
            results['inchi'] = input_value
            
            # Try to extract molecular formula from InChI
            formula_match = re.search(r'/([CH][0-9]*[A-Z][0-9A-Za-z]*)', input_value)
            if formula_match:
                formula = formula_match.group(1)
                results['molecular_formula'] = formula
                results['molecular_weight'] = analyzer.calculate_molecular_weight_from_formula(formula)
            
        elif input_type.lower() == 'formula':
            # Molecular formula analysis
            results['molecular_formula'] = input_value
            results['molecular_weight'] = analyzer.calculate_molecular_weight_from_formula(input_value)
        
        else:
            results['success'] = False
            results['error'] = f"Unsupported input type: {input_type}"
    
    except Exception as e:
        results['success'] = False
        results['error'] = str(e)
        logging.error(f"Error in molecular analysis: {e}")
    
    return results

def generate_2d_structure(smiles: str) -> Optional[str]:
    """Generate a simple 2D structure representation (as SVG coordinates)"""
    # This is a placeholder for 2D structure generation
    # In a real implementation, you would use RDKit or similar
    
    try:
        # Basic atom positioning for simple molecules
        atoms = []
        bonds = []
        
        # Very simplified positioning logic
        x_pos = 50
        y_pos = 50
        
        # Parse atoms from SMILES (very basic)
        atom_pattern = r'[A-Z][a-z]?'
        atom_matches = re.findall(atom_pattern, smiles)
        
        for i, atom in enumerate(atom_matches):
            atoms.append({
                'symbol': atom,
                'x': x_pos + i * 40,
                'y': y_pos + (i % 2) * 20,
                'id': i
            })
        
        # Simple bonds between consecutive atoms
        for i in range(len(atoms) - 1):
            bonds.append({
                'from': i,
                'to': i + 1,
                'type': 'single'
            })
        
        return json.dumps({
            'atoms': atoms,
            'bonds': bonds,
            'width': max(200, len(atoms) * 40 + 100),
            'height': 150
        })
    
    except Exception as e:
        logging.error(f"Error generating 2D structure: {e}")
        return None

def validate_smiles(smiles: str) -> bool:
    """Basic SMILES validation"""
    if not smiles or not isinstance(smiles, str):
        return False
    
    # Check for balanced brackets
    stack = []
    bracket_pairs = {'(': ')', '[': ']'}
    
    for char in smiles:
        if char in bracket_pairs:
            stack.append(char)
        elif char in bracket_pairs.values():
            if not stack:
                return False
            if bracket_pairs.get(stack.pop()) != char:
                return False
    
    return len(stack) == 0

def validate_inchi(inchi: str) -> bool:
    """Basic InChI validation"""
    if not inchi or not isinstance(inchi, str):
        return False
    
    return inchi.startswith('InChI=')
