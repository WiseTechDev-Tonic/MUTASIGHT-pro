// DNA/RNA 3D Visualization using Three.js
class DNARNAViewer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.dnaModel = null;
        this.animationId = null;
        this.rotationEnabled = true;
        
        this.initialize();
    }
    
    initialize() {
        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0a0a);
        
        // Create camera
        this.camera = new THREE.PerspectiveCamera(
            75,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(0, 0, 10);
        
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
        const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
        this.scene.add(ambientLight);
        
        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        this.scene.add(directionalLight);
        
        // Point lights for color
        const pointLight1 = new THREE.PointLight(0x00ff00, 0.3, 100);
        pointLight1.position.set(5, 5, 5);
        this.scene.add(pointLight1);
        
        const pointLight2 = new THREE.PointLight(0x0077ff, 0.3, 100);
        pointLight2.position.set(-5, -5, 5);
        this.scene.add(pointLight2);
    }
    
    createDNAHelix(sequence, sequenceType = 'dna') {
        this.clearScene();
        
        const group = new THREE.Group();
        const helixRadius = 2;
        const helixHeight = sequence.length * 0.5;
        const turns = sequence.length / 10; // One complete turn per 10 base pairs
        
        // Base pair colors
        const baseColors = {
            'A': 0xff4444,  // Red
            'T': 0x44ff44,  // Green
            'U': 0x44ff44,  // Green (for RNA)
            'G': 0x4444ff,  // Blue
            'C': 0xffff44   // Yellow
        };
        
        // Create backbone strands
        const backboneGeometry = new THREE.CylinderGeometry(0.1, 0.1, helixHeight, 8);
        const backboneMaterial1 = new THREE.MeshPhongMaterial({ 
            color: 0x888888, 
            transparent: true, 
            opacity: 0.7 
        });
        const backboneMaterial2 = new THREE.MeshPhongMaterial({ 
            color: 0xaaaaaa, 
            transparent: true, 
            opacity: 0.7 
        });
        
        const backbone1 = new THREE.Mesh(backboneGeometry, backboneMaterial1);
        const backbone2 = new THREE.Mesh(backboneGeometry, backboneMaterial2);
        
        // Position backbones
        backbone1.position.set(helixRadius, 0, 0);
        backbone2.position.set(-helixRadius, 0, 0);
        
        group.add(backbone1);
        group.add(backbone2);
        
        // Create base pairs
        for (let i = 0; i < sequence.length; i++) {
            const base = sequence[i].toUpperCase();
            if (!baseColors[base]) continue;
            
            const angle = (i / sequence.length) * turns * Math.PI * 2;
            const y = (i / sequence.length) * helixHeight - helixHeight / 2;
            
            // Create base sphere
            const baseGeometry = new THREE.SphereGeometry(0.3, 16, 16);
            const baseMaterial = new THREE.MeshPhongMaterial({ 
                color: baseColors[base],
                shininess: 100
            });
            const baseMesh = new THREE.Mesh(baseGeometry, baseMaterial);
            
            // Position base on helix
            const x1 = Math.cos(angle) * helixRadius;
            const z1 = Math.sin(angle) * helixRadius;
            baseMesh.position.set(x1, y, z1);
            
            // Add base pair connection
            const complementaryBase = this.getComplementaryBase(base, sequenceType);
            if (complementaryBase) {
                const compGeometry = new THREE.SphereGeometry(0.25, 16, 16);
                const compMaterial = new THREE.MeshPhongMaterial({ 
                    color: baseColors[complementaryBase],
                    shininess: 100
                });
                const compMesh = new THREE.Mesh(compGeometry, compMaterial);
                
                const x2 = Math.cos(angle + Math.PI) * helixRadius;
                const z2 = Math.sin(angle + Math.PI) * helixRadius;
                compMesh.position.set(x2, y, z2);
                
                // Create hydrogen bond connection
                const bondGeometry = new THREE.CylinderGeometry(0.05, 0.05, helixRadius * 2, 6);
                const bondMaterial = new THREE.MeshPhongMaterial({ 
                    color: 0x666666,
                    transparent: true,
                    opacity: 0.5
                });
                const bondMesh = new THREE.Mesh(bondGeometry, bondMaterial);
                bondMesh.position.set(0, y, 0);
                bondMesh.rotation.z = Math.PI / 2;
                bondMesh.rotation.y = angle;
                
                group.add(compMesh);
                group.add(bondMesh);
            }
            
            group.add(baseMesh);
            
            // Store base information for interaction
            baseMesh.userData = {
                base: base,
                position: i,
                complementary: complementaryBase
            };
        }
        
        this.dnaModel = group;
        this.scene.add(group);
        
        // Center the model
        this.centerModel();
    }
    
    getComplementaryBase(base, sequenceType) {
        const complements = {
            'dna': { 'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G' },
            'rna': { 'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G' }
        };
        
        return complements[sequenceType] ? complements[sequenceType][base] : null;
    }
    
    createProteinStructure(sequence) {
        this.clearScene();
        
        const group = new THREE.Group();
        const aminoAcidColors = {
            'A': 0xff0000, 'R': 0x00ff00, 'N': 0x0000ff, 'D': 0xffff00,
            'C': 0xff00ff, 'E': 0x00ffff, 'Q': 0x800000, 'G': 0x008000,
            'H': 0x000080, 'I': 0x808000, 'L': 0x800080, 'K': 0x008080,
            'M': 0xc0c0c0, 'F': 0x404040, 'P': 0xff8080, 'S': 0x80ff80,
            'T': 0x8080ff, 'W': 0xffff80, 'Y': 0xff80ff, 'V': 0x80ffff
        };
        
        // Create backbone
        const points = [];
        for (let i = 0; i < sequence.length; i++) {
            const angle = (i / sequence.length) * Math.PI * 4;
            const radius = 3 + Math.sin(angle * 2) * 0.5;
            const x = Math.cos(angle) * radius;
            const y = i * 0.3 - sequence.length * 0.15;
            const z = Math.sin(angle) * radius;
            points.push(new THREE.Vector3(x, y, z));
        }
        
        const curve = new THREE.CatmullRomCurve3(points);
        const tubeGeometry = new THREE.TubeGeometry(curve, points.length * 2, 0.2, 8, false);
        const tubeMaterial = new THREE.MeshPhongMaterial({ 
            color: 0x666666,
            shininess: 100
        });
        const tube = new THREE.Mesh(tubeGeometry, tubeMaterial);
        group.add(tube);
        
        // Add amino acid spheres
        for (let i = 0; i < sequence.length; i++) {
            const aa = sequence[i].toUpperCase();
            const color = aminoAcidColors[aa] || 0x888888;
            
            const aaGeometry = new THREE.SphereGeometry(0.4, 16, 16);
            const aaMaterial = new THREE.MeshPhongMaterial({ 
                color: color,
                shininess: 100
            });
            const aaMesh = new THREE.Mesh(aaGeometry, aaMaterial);
            
            const point = curve.getPoint(i / (sequence.length - 1));
            aaMesh.position.copy(point);
            
            aaMesh.userData = {
                aminoAcid: aa,
                position: i
            };
            
            group.add(aaMesh);
        }
        
        this.dnaModel = group;
        this.scene.add(group);
        this.centerModel();
    }
    
    clearScene() {
        if (this.dnaModel) {
            this.scene.remove(this.dnaModel);
            this.dnaModel = null;
        }
    }
    
    centerModel() {
        if (this.dnaModel) {
            const box = new THREE.Box3().setFromObject(this.dnaModel);
            const center = box.getCenter(new THREE.Vector3());
            this.dnaModel.position.sub(center);
            
            const size = box.getSize(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);
            const fov = this.camera.fov * (Math.PI / 180);
            let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
            cameraZ *= 1.5; // Zoom out a bit
            
            this.camera.position.z = cameraZ;
            this.camera.lookAt(0, 0, 0);
        }
    }
    
    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        
        if (this.rotationEnabled && this.dnaModel) {
            this.dnaModel.rotation.y += 0.01;
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
        this.camera.position.set(0, 0, 10);
        this.camera.lookAt(0, 0, 0);
        if (this.controls) {
            this.controls.reset();
        }
        this.centerModel();
    }
    
    toggleWireframe() {
        if (this.dnaModel) {
            this.dnaModel.traverse((child) => {
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

// Global viewer instance
let dnaViewer = null;

function initializeDNAViewer(sequence, sequenceType = 'dna') {
    if (dnaViewer) {
        dnaViewer.dispose();
    }
    
    dnaViewer = new DNARNAViewer('dnaViewer3D');
    
    if (sequenceType === 'protein') {
        dnaViewer.createProteinStructure(sequence);
    } else {
        dnaViewer.createDNAHelix(sequence, sequenceType);
    }
}

// Control functions for the viewer
function toggleRotation() {
    if (dnaViewer) {
        dnaViewer.toggleRotation();
    }
}

function resetView() {
    if (dnaViewer) {
        dnaViewer.resetView();
    }
}

function toggleWireframe() {
    if (dnaViewer) {
        dnaViewer.toggleWireframe();
    }
}