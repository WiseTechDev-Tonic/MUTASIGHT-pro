/**
 * Molecular Viewer - JavaScript utilities for molecular structure visualization
 * Part of MutaSight AI Drug Discovery Platform
 */

class MolecularViewer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.svg = null;
        this.width = 400;
        this.height = 300;
        this.atoms = [];
        this.bonds = [];
        this.scale = 1;
        this.offsetX = 0;
        this.offsetY = 0;
    }

    /**
     * Initialize the SVG container
     */
    init() {
        if (!this.container) {
            console.error('Molecular viewer container not found');
            return;
        }

        this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        this.svg.setAttribute('width', this.width);
        this.svg.setAttribute('height', this.height);
        this.svg.setAttribute('viewBox', `0 0 ${this.width} ${this.height}`);
        this.svg.style.background = 'white';
        this.svg.style.border = '1px solid #ddd';
        this.svg.style.borderRadius = '8px';

        this.container.innerHTML = '';
        this.container.appendChild(this.svg);

        // Add zoom and pan functionality
        this.addInteractivity();
    }

    /**
     * Parse SMILES notation and generate 2D coordinates
     */
    parseSMILES(smiles) {
        this.atoms = [];
        this.bonds = [];

        // Simple SMILES parsing - this is a basic implementation
        // In production, you would use a proper chemistry library
        let atomIndex = 0;
        let x = 50;
        let y = this.height / 2;
        const bondLength = 40;

        // Remove brackets and special characters for simple parsing
        const simplifiedSMILES = smiles.replace(/[\[\]()=]/g, '');
        
        for (let i = 0; i < simplifiedSMILES.length; i++) {
            const char = simplifiedSMILES[i];
            
            if (this.isAtom(char)) {
                // Handle two-letter atoms
                let atomSymbol = char;
                if (i + 1 < simplifiedSMILES.length && 
                    simplifiedSMILES[i + 1].toLowerCase() === simplifiedSMILES[i + 1]) {
                    atomSymbol += simplifiedSMILES[i + 1];
                    i++; // Skip next character
                }

                this.atoms.push({
                    id: atomIndex,
                    symbol: atomSymbol,
                    x: x,
                    y: y,
                    color: this.getAtomColor(atomSymbol)
                });

                // Add bond to previous atom (if exists)
                if (atomIndex > 0) {
                    this.bonds.push({
                        from: atomIndex - 1,
                        to: atomIndex,
                        type: 'single'
                    });
                }

                atomIndex++;
                x += bondLength;
                
                // Wrap around if too wide
                if (x > this.width - 50) {
                    x = 50;
                    y += 60;
                }
            }
        }

        this.render();
    }

    /**
     * Check if character represents an atom
     */
    isAtom(char) {
        return /[A-Z]/.test(char);
    }

    /**
     * Get color for atom based on element
     */
    getAtomColor(symbol) {
        const colors = {
            'C': '#404040',
            'N': '#3050f8',
            'O': '#ff0d0d',
            'S': '#ffff30',
            'P': '#ff8000',
            'F': '#90e050',
            'Cl': '#1ff01f',
            'Br': '#a62929',
            'I': '#940094',
            'H': '#ffffff'
        };
        return colors[symbol] || '#ff1493';
    }

    /**
     * Render the molecular structure
     */
    render() {
        if (!this.svg) return;

        // Clear previous content
        this.svg.innerHTML = '';

        // Create definition for bond styles
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        this.svg.appendChild(defs);

        // Render bonds first (so they appear behind atoms)
        this.renderBonds();

        // Render atoms
        this.renderAtoms();

        // Add title
        this.addTitle();
    }

    /**
     * Render chemical bonds
     */
    renderBonds() {
        this.bonds.forEach(bond => {
            const fromAtom = this.atoms[bond.from];
            const toAtom = this.atoms[bond.to];

            if (!fromAtom || !toAtom) return;

            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', fromAtom.x);
            line.setAttribute('y1', fromAtom.y);
            line.setAttribute('x2', toAtom.x);
            line.setAttribute('y2', toAtom.y);
            line.setAttribute('stroke', '#404040');
            line.setAttribute('stroke-width', bond.type === 'double' ? '3' : '2');
            line.setAttribute('stroke-linecap', 'round');

            this.svg.appendChild(line);
        });
    }

    /**
     * Render atoms
     */
    renderAtoms() {
        this.atoms.forEach(atom => {
            // Atom circle
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', atom.x);
            circle.setAttribute('cy', atom.y);
            circle.setAttribute('r', atom.symbol === 'H' ? '8' : '12');
            circle.setAttribute('fill', atom.color);
            circle.setAttribute('stroke', '#404040');
            circle.setAttribute('stroke-width', '1');
            circle.setAttribute('class', 'atom-circle');

            // Atom label
            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('x', atom.x);
            text.setAttribute('y', atom.y + 4);
            text.setAttribute('text-anchor', 'middle');
            text.setAttribute('font-family', 'Arial, sans-serif');
            text.setAttribute('font-size', '12');
            text.setAttribute('font-weight', 'bold');
            text.setAttribute('fill', atom.symbol === 'H' ? '#000' : '#fff');
            text.textContent = atom.symbol;

            // Add hover effects
            circle.addEventListener('mouseenter', () => this.highlightAtom(atom));
            circle.addEventListener('mouseleave', () => this.unhighlightAtom());

            this.svg.appendChild(circle);
            this.svg.appendChild(text);
        });
    }

    /**
     * Add title to the structure
     */
    addTitle() {
        const title = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        title.setAttribute('x', this.width / 2);
        title.setAttribute('y', 20);
        title.setAttribute('text-anchor', 'middle');
        title.setAttribute('font-family', 'Arial, sans-serif');
        title.setAttribute('font-size', '14');
        title.setAttribute('font-weight', 'bold');
        title.setAttribute('fill', '#666');
        title.textContent = '2D Molecular Structure';

        this.svg.appendChild(title);
    }

    /**
     * Highlight atom on hover
     */
    highlightAtom(atom) {
        // Create tooltip
        const tooltip = document.createElement('div');
        tooltip.id = 'atom-tooltip';
        tooltip.style.position = 'absolute';
        tooltip.style.background = 'rgba(0,0,0,0.8)';
        tooltip.style.color = 'white';
        tooltip.style.padding = '5px 10px';
        tooltip.style.borderRadius = '4px';
        tooltip.style.fontSize = '12px';
        tooltip.style.pointerEvents = 'none';
        tooltip.style.zIndex = '1000';
        tooltip.textContent = `${atom.symbol} (${atom.id})`;

        document.body.appendChild(tooltip);

        // Position tooltip
        document.addEventListener('mousemove', this.updateTooltipPosition);
    }

    /**
     * Remove atom highlight
     */
    unhighlightAtom() {
        const tooltip = document.getElementById('atom-tooltip');
        if (tooltip) {
            tooltip.remove();
            document.removeEventListener('mousemove', this.updateTooltipPosition);
        }
    }

    /**
     * Update tooltip position
     */
    updateTooltipPosition(event) {
        const tooltip = document.getElementById('atom-tooltip');
        if (tooltip) {
            tooltip.style.left = (event.pageX + 10) + 'px';
            tooltip.style.top = (event.pageY - 30) + 'px';
        }
    }

    /**
     * Add zoom and pan functionality
     */
    addInteractivity() {
        let isPanning = false;
        let startX, startY;

        this.svg.addEventListener('mousedown', (e) => {
            if (e.button === 0) { // Left mouse button
                isPanning = true;
                startX = e.clientX - this.offsetX;
                startY = e.clientY - this.offsetY;
                this.svg.style.cursor = 'grabbing';
            }
        });

        this.svg.addEventListener('mousemove', (e) => {
            if (isPanning) {
                this.offsetX = e.clientX - startX;
                this.offsetY = e.clientY - startY;
                this.updateTransform();
            }
        });

        this.svg.addEventListener('mouseup', () => {
            isPanning = false;
            this.svg.style.cursor = 'grab';
        });

        this.svg.addEventListener('mouseleave', () => {
            isPanning = false;
            this.svg.style.cursor = 'default';
        });

        // Zoom functionality
        this.svg.addEventListener('wheel', (e) => {
            e.preventDefault();
            const delta = e.deltaY > 0 ? 0.9 : 1.1;
            this.scale *= delta;
            this.scale = Math.max(0.5, Math.min(3, this.scale));
            this.updateTransform();
        });

        this.svg.style.cursor = 'grab';
    }

    /**
     * Update SVG transform
     */
    updateTransform() {
        const g = this.svg.querySelector('g.transform-group');
        if (g) {
            g.setAttribute('transform', 
                `translate(${this.offsetX}, ${this.offsetY}) scale(${this.scale})`);
        }
    }

    /**
     * Reset view to default
     */
    resetView() {
        this.scale = 1;
        this.offsetX = 0;
        this.offsetY = 0;
        this.updateTransform();
    }

    /**
     * Export structure as SVG string
     */
    exportSVG() {
        return new XMLSerializer().serializeToString(this.svg);
    }

    /**
     * Load structure from data
     */
    loadStructureData(data) {
        if (data.atoms && data.bonds) {
            this.atoms = data.atoms;
            this.bonds = data.bonds;
            this.render();
        }
    }

    /**
     * Clear the viewer
     */
    clear() {
        if (this.svg) {
            this.svg.innerHTML = '';
        }
        this.atoms = [];
        this.bonds = [];
    }
}

// Utility functions for molecular analysis
const MolecularUtils = {
    /**
     * Calculate molecular weight from formula
     */
    calculateMolecularWeight(formula) {
        const atomicWeights = {
            'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998,
            'P': 30.974, 'S': 32.065, 'Cl': 35.453, 'Br': 79.904, 'I': 126.904,
            'Na': 22.990, 'K': 39.098, 'Mg': 24.305, 'Ca': 40.078
        };

        let weight = 0;
        const matches = formula.match(/([A-Z][a-z]?)(\d*)/g);
        
        if (matches) {
            matches.forEach(match => {
                const element = match.match(/[A-Z][a-z]?/)[0];
                const count = match.match(/\d+/);
                const num = count ? parseInt(count[0]) : 1;
                
                if (atomicWeights[element]) {
                    weight += atomicWeights[element] * num;
                }
            });
        }

        return Math.round(weight * 100) / 100;
    },

    /**
     * Validate SMILES notation
     */
    validateSMILES(smiles) {
        if (!smiles || typeof smiles !== 'string') return false;
        
        // Check for balanced brackets
        let roundBrackets = 0;
        let squareBrackets = 0;
        
        for (let char of smiles) {
            if (char === '(') roundBrackets++;
            else if (char === ')') roundBrackets--;
            else if (char === '[') squareBrackets++;
            else if (char === ']') squareBrackets--;
            
            if (roundBrackets < 0 || squareBrackets < 0) return false;
        }
        
        return roundBrackets === 0 && squareBrackets === 0;
    },

    /**
     * Format molecular formula for display
     */
    formatMolecularFormula(formula) {
        return formula.replace(/(\d+)/g, '<sub>$1</sub>');
    },

    /**
     * Generate example molecules
     */
    getExampleMolecules() {
        return [
            { name: 'Ethanol', smiles: 'CCO', formula: 'C2H6O' },
            { name: 'Acetic Acid', smiles: 'CC(=O)O', formula: 'C2H4O2' },
            { name: 'Benzene', smiles: 'c1ccccc1', formula: 'C6H6' },
            { name: 'Ibuprofen', smiles: 'CC(C)CC1=CC=C(C=C1)C(C)C(=O)O', formula: 'C13H18O2' },
            { name: 'Paracetamol', smiles: 'CC(=O)NC1=CC=C(C=C1)O', formula: 'C8H9NO2' },
            { name: 'Aspirin', smiles: 'CC(=O)OC1=CC=CC=C1C(=O)O', formula: 'C9H8O4' }
        ];
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MolecularViewer, MolecularUtils };
}
