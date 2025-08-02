// 3D Molecular Visualization using Three.js
class Molecular3DViewer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.molecularModel = null;
        this.animationId = null;
        this.rotationEnabled = true;
        this.renderMode = 'ball-stick'; // ball-stick, wireframe, space-fill
        
        this.initialize();
    }
    
    initialize() {
        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a1a);
        
        // Create camera
        this.camera = new THREE.PerspectiveCamera(
            75,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(0, 0, 15);
        
        // Create renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);
        
        // Add lights
        this.addLights();
        
        // Add orbit controls if available
        if (typeof THREE.OrbitControls !== 'undefined') {
            this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
            this.controls.enableDamping = true;
            this.controls.dampingFactor = 0.05;
        }
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize(), false);
        
        // Start animation loop
        this.animate();
    }
    
    addLights() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);
        
        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        directionalLight.castShadow = true;
        this.scene.add(directionalLight);
        
        // Point lights for better illumination
        const pointLight1 = new THREE.PointLight(0x007bff, 0.4, 100);
        pointLight1.position.set(5, 5, 5);
        this.scene.add(pointLight1);
        
        const pointLight2 = new THREE.PointLight(0x17a2b8, 0.4, 100);
        pointLight2.position.set(-5, -5, 5);
        this.scene.add(pointLight2);
    }
    
    createMoleculeFromSMILES(smiles) {
        this.clearScene();
        
        // Parse SMILES and create 3D representation
        // This is a simplified implementation - in production, you'd use RDKit.js or similar
        const molecule = this.parseSMILES(smiles);
        this.renderMolecule(molecule);
    }
    
    parseSMILES(smiles) {
        // Simplified SMILES parser for common molecules
        const atoms = [];
        const bonds = [];
        
        // Common atom mapping
        const atomicRadii = {
            'C': 0.7, 'N': 0.65, 'O': 0.6, 'H': 0.31,
            'S': 1.05, 'P': 1.0, 'F': 0.5, 'Cl': 0.99, 'Br': 1.14, 'I': 1.33
        };
        
        const atomicColors = {
            'C': 0x404040,   // Dark gray
            'N': 0x3050f8,   // Blue
            'O': 0xff0d0d,   // Red
            'H': 0xffffff,   // White
            'S': 0xffff30,   // Yellow
            'P': 0xff8000,   // Orange
            'F': 0x90e050,   // Light green
            'Cl': 0x1ff01f,  // Green
            'Br': 0xa62929,  // Brown
            'I': 0x940094    // Purple
        };
        
        // Generate a simple 3D structure based on SMILES
        // This is a placeholder - real implementation would need proper chemistry libraries
        let atomIndex = 0;
        let x = 0, y = 0, z = 0;
        
        for (let i = 0; i < smiles.length; i++) {
            const char = smiles[i];
            
            if (char.match(/[A-Z]/)) {
                // Found an atom
                let atomSymbol = char;
                if (i + 1 < smiles.length && smiles[i + 1].match(/[a-z]/)) {
                    atomSymbol += smiles[i + 1];
                    i++; // Skip the lowercase letter
                }
                
                atoms.push({
                    symbol: atomSymbol,
                    position: new THREE.Vector3(x, y, z),
                    radius: atomicRadii[atomSymbol] || 0.6,
                    color: atomicColors[atomSymbol] || 0x888888,
                    index: atomIndex
                });
                
                // Connect to previous atom (simplified bonding)
                if (atomIndex > 0) {
                    bonds.push({
                        from: atomIndex - 1,
                        to: atomIndex,
                        order: 1
                    });
                }
                
                atomIndex++;
                x += 1.5; // Simple linear arrangement
                
                // Add some variation for ring structures
                if (char === 'C' && Math.random() > 0.7) {
                    y += (Math.random() - 0.5) * 2;
                    z += (Math.random() - 0.5) * 2;
                }
            }
        }
        
        // If no atoms were parsed, create a simple ethanol molecule as example
        if (atoms.length === 0) {
            atoms.push(
                { symbol: 'C', position: new THREE.Vector3(0, 0, 0), radius: 0.7, color: 0x404040, index: 0 },
                { symbol: 'C', position: new THREE.Vector3(1.5, 0, 0), radius: 0.7, color: 0x404040, index: 1 },
                { symbol: 'O', position: new THREE.Vector3(3, 0, 0), radius: 0.6, color: 0xff0d0d, index: 2 },
                { symbol: 'H', position: new THREE.Vector3(-1, 0, 0), radius: 0.31, color: 0xffffff, index: 3 },
                { symbol: 'H', position: new THREE.Vector3(0, 1, 0), radius: 0.31, color: 0xffffff, index: 4 },
                { symbol: 'H', position: new THREE.Vector3(0, -1, 0), radius: 0.31, color: 0xffffff, index: 5 },
                { symbol: 'H', position: new THREE.Vector3(1.5, 1, 0), radius: 0.31, color: 0xffffff, index: 6 },
                { symbol: 'H', position: new THREE.Vector3(1.5, -1, 0), radius: 0.31, color: 0xffffff, index: 7 },
                { symbol: 'H', position: new THREE.Vector3(3.5, 0, 0), radius: 0.31, color: 0xffffff, index: 8 }
            );
            
            bonds.push(
                { from: 0, to: 1, order: 1 },
                { from: 1, to: 2, order: 1 },
                { from: 0, to: 3, order: 1 },
                { from: 0, to: 4, order: 1 },
                { from: 0, to: 5, order: 1 },
                { from: 1, to: 6, order: 1 },
                { from: 1, to: 7, order: 1 },
                { from: 2, to: 8, order: 1 }
            );
        }
        
        return { atoms, bonds };
    }
    
    renderMolecule(molecule) {
        const group = new THREE.Group();
        const { atoms, bonds } = molecule;
        
        // Store atom meshes for bond creation
        const atomMeshes = [];
        
        // Create atoms
        atoms.forEach(atom => {
            const geometry = new THREE.SphereGeometry(atom.radius, 32, 32);
            const material = new THREE.MeshPhongMaterial({ 
                color: atom.color,
                shininess: 100
            });
            const atomMesh = new THREE.Mesh(geometry, material);
            atomMesh.position.copy(atom.position);
            atomMesh.castShadow = true;
            atomMesh.receiveShadow = true;
            
            // Store atom data
            atomMesh.userData = {
                symbol: atom.symbol,
                index: atom.index
            };
            
            group.add(atomMesh);
            atomMeshes[atom.index] = atomMesh;
        });
        
        // Create bonds
        bonds.forEach(bond => {
            const fromAtom = atoms[bond.from];
            const toAtom = atoms[bond.to];
            
            if (fromAtom && toAtom) {
                // Calculate bond direction and length
                const direction = new THREE.Vector3().subVectors(toAtom.position, fromAtom.position);
                const length = direction.length();
                const midpoint = new THREE.Vector3().addVectors(fromAtom.position, toAtom.position).multiplyScalar(0.5);
                
                // Create bond cylinder
                const bondRadius = bond.order === 1 ? 0.1 : bond.order === 2 ? 0.08 : 0.06;
                const bondGeometry = new THREE.CylinderGeometry(bondRadius, bondRadius, length, 8);
                const bondMaterial = new THREE.MeshPhongMaterial({ 
                    color: 0x666666,
                    shininess: 50
                });
                const bondMesh = new THREE.Mesh(bondGeometry, bondMaterial);
                
                // Position and orient the bond
                bondMesh.position.copy(midpoint);
                bondMesh.lookAt(toAtom.position);
                bondMesh.rotateX(Math.PI / 2);
                
                group.add(bondMesh);
                
                // For double/triple bonds, add additional cylinders
                if (bond.order > 1) {
                    for (let i = 1; i < bond.order; i++) {
                        const extraBond = bondMesh.clone();
                        const offset = new THREE.Vector3(0, 0, i * 0.3 - (bond.order - 1) * 0.15);
                        extraBond.position.add(offset);
                        group.add(extraBond);
                    }
                }
            }
        });
        
        this.molecularModel = group;
        this.scene.add(group);
        this.centerModel();
    }
    
    changeRenderMode() {
        if (this.renderMode === 'ball-stick') {
            this.renderMode = 'wireframe';
            this.toggleWireframe();
        } else if (this.renderMode === 'wireframe') {
            this.renderMode = 'space-fill';
            this.setSpaceFillMode();
        } else {
            this.renderMode = 'ball-stick';
            this.setBallStickMode();
        }
    }
    
    setSpaceFillMode() {
        if (this.molecularModel) {
            this.molecularModel.traverse((child) => {
                if (child.isMesh && child.userData.symbol) {
                    // Make atoms larger for space-fill mode
                    child.scale.setScalar(2.0);
                    child.material.wireframe = false;
                } else if (child.isMesh) {
                    // Hide bonds in space-fill mode
                    child.visible = false;
                }
            });
        }
    }
    
    setBallStickMode() {
        if (this.molecularModel) {
            this.molecularModel.traverse((child) => {
                if (child.isMesh && child.userData.symbol) {
                    // Normal atom size
                    child.scale.setScalar(1.0);
                    child.material.wireframe = false;
                    child.visible = true;
                } else if (child.isMesh) {
                    // Show bonds
                    child.visible = true;
                    child.material.wireframe = false;
                }
            });
        }
    }
    
    clearScene() {
        if (this.molecularModel) {
            this.scene.remove(this.molecularModel);
            this.molecularModel = null;
        }
    }
    
    centerModel() {
        if (this.molecularModel) {
            const box = new THREE.Box3().setFromObject(this.molecularModel);
            const center = box.getCenter(new THREE.Vector3());
            this.molecularModel.position.sub(center);
            
            const size = box.getSize(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);
            const fov = this.camera.fov * (Math.PI / 180);
            let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
            cameraZ *= 2; // Zoom out a bit
            
            this.camera.position.z = cameraZ;
            this.camera.lookAt(0, 0, 0);
        }
    }
    
    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        
        if (this.rotationEnabled && this.molecularModel) {
            this.molecularModel.rotation.y += 0.005;
        }
        
        if (this.controls) {
            this.controls.update();
        }
        
        this.renderer.render(this.scene, this.camera);
    }
    
    toggleRotation() {
        this.rotationEnabled = !this.rotationEnabled;
    }
    
    resetView() {
        this.camera.position.set(0, 0, 15);
        this.camera.lookAt(0, 0, 0);
        if (this.controls) {
            this.controls.reset();
        }
        this.centerModel();
    }
    
    toggleWireframe() {
        if (this.molecularModel) {
            this.molecularModel.traverse((child) => {
                if (child.isMesh && child.material) {
                    child.material.wireframe = !child.material.wireframe;
                }
            });
        }
    }
    
    onWindowResize() {
        const width = this.container.clientWidth;
        const height = this.container.clientHeight;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }
    
    dispose() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        
        if (this.renderer) {
            this.renderer.dispose();
            this.container.removeChild(this.renderer.domElement);
        }
        
        if (this.controls) {
            this.controls.dispose();
        }
    }
}

// Global molecular viewer instance
let molecularViewer = null;

function initializeMolecularViewer(smiles) {
    if (molecularViewer) {
        molecularViewer.dispose();
    }
    
    molecularViewer = new Molecular3DViewer('molecularViewer3D');
    molecularViewer.createMoleculeFromSMILES(smiles);
}

// Control functions for the molecular viewer
function toggleMolecularRotation() {
    if (molecularViewer) {
        molecularViewer.toggleRotation();
    }
}

function resetMolecularView() {
    if (molecularViewer) {
        molecularViewer.resetView();
    }
}

function toggleMolecularWireframe() {
    if (molecularViewer) {
        molecularViewer.toggleWireframe();
    }
}

function changeRenderMode() {
    if (molecularViewer) {
        molecularViewer.changeRenderMode();
    }
}