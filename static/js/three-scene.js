/* =====================================================
   HUMISENSE - Three.js 3D Experience
   Interactive AI Orb, Neural Network, and Visualizations
   ===================================================== */

class ThreeScene {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            antialias: true,
            alpha: true,
            ...options
        };
        
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.animationId = null;
        this.clock = new THREE.Clock();
        this.mouse = new THREE.Vector2();
        this.raycaster = new THREE.Raycaster();
        this.hoveredObject = null;
        
        this.init();
    }
    
    init() {
        this.setupScene();
        this.setupCamera();
        this.setupRenderer();
        this.setupLights();
        this.setupPostProcessing();
        this.setupEventListeners();
        this.animate();
    }
    
    setupScene() {
        this.scene = new THREE.Scene();
        this.scene.fog = new THREE.Fog(0x030712, 5, 50);
    }
    
    setupCamera() {
        const aspect = window.innerWidth / window.innerHeight;
        this.camera = new THREE.PerspectiveCamera(60, aspect, 0.1, 1000);
        this.camera.position.z = 30;
    }
    
    setupRenderer() {
        this.renderer = new THREE.WebGLRenderer({
            antialias: this.options.antialias,
            alpha: this.options.alpha,
            powerPreference: 'high-performance'
        });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.setClearColor(0x000000, 0);
        this.container.appendChild(this.renderer.domElement);
    }
    
    setupLights() {
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        this.scene.add(ambientLight);
        
        const pointLight1 = new THREE.PointLight(0x6366f1, 2, 100);
        pointLight1.position.set(10, 10, 10);
        this.scene.add(pointLight1);
        
        const pointLight2 = new THREE.PointLight(0x06b6d4, 2, 100);
        pointLight2.position.set(-10, -10, 10);
        this.scene.add(pointLight2);
    }
    
    setupPostProcessing() {
        // Optional: Add bloom effect
        // This would require additional post-processing imports
    }
    
    setupEventListeners() {
        window.addEventListener('resize', this.onResize.bind(this));
        window.addEventListener('mousemove', this.onMouseMove.bind(this));
    }
    
    onResize() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }
    
    onMouseMove(event) {
        this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    }
    
    animate() {
        this.animationId = requestAnimationFrame(this.animate.bind(this));
        const delta = this.clock.getDelta();
        const elapsed = this.clock.getElapsedTime();
        
        this.update(delta, elapsed);
        this.renderer.render(this.scene, this.camera);
    }
    
    update(delta, elapsed) {
        // Override in subclasses
    }
    
    dispose() {
        cancelAnimationFrame(this.animationId);
        window.removeEventListener('resize', this.onResize);
        window.removeEventListener('mousemove', this.onMouseMove);
        this.renderer.dispose();
        this.container.removeChild(this.renderer.domElement);
    }
}

/* =====================================================
   AI ORB - Interactive Neural Network Sphere
   ===================================================== */
class AIOrb extends ThreeScene {
    constructor(container) {
        super(container);
        this.particles = [];
        this.orbs = [];
        this.connections = [];
        this.time = 0;
    }
    
    setupScene() {
        super.setupScene();
        this.createOrb();
        this.createParticles();
        this.createConnections();
    }
    
    createOrb() {
        // Main orb geometry
        const geometry = new THREE.SphereGeometry(5, 64, 64);
        
        // Custom shader material for ethereal look
        const material = new THREE.ShaderMaterial({
            uniforms: {
                time: { value: 0 },
                color1: { value: new THREE.Color(0x6366f1) },
                color2: { value: new THREE.Color(0x8b5cf6) },
                color3: { value: new THREE.Color(0x06b6d4) },
            },
            vertexShader: `
                varying vec3 vNormal;
                varying vec3 vPosition;
                uniform float time;
                
                void main() {
                    vNormal = normal;
                    vPosition = position;
                    
                    // Subtle vertex displacement
                    vec3 pos = position;
                    float displacement = sin(pos.x * 2.0 + time) * 
                                        cos(pos.y * 2.0 + time) * 
                                        sin(pos.z * 2.0 + time) * 0.1;
                    pos += normal * displacement;
                    
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
                }
            `,
            fragmentShader: `
                uniform float time;
                uniform vec3 color1;
                uniform vec3 color2;
                uniform vec3 color3;
                varying vec3 vNormal;
                varying vec3 vPosition;
                
                void main() {
                    // Fresnel effect
                    vec3 viewDirection = normalize(cameraPosition - vPosition);
                    float fresnel = pow(1.0 - dot(viewDirection, vNormal), 3.0);
                    
                    // Animated gradient
                    float gradient = sin(vPosition.x * 0.5 + time) * 
                                   cos(vPosition.y * 0.5 + time) * 0.5 + 0.5;
                    
                    vec3 color = mix(color1, color2, gradient);
                    color = mix(color, color3, fresnel * 0.5);
                    
                    // Glow effect
                    float glow = fresnel * 0.8 + 0.2;
                    
                    gl_FragColor = vec4(color, glow);
                }
            `,
            transparent: true,
            side: THREE.DoubleSide,
        });
        
        this.orb = new THREE.Mesh(geometry, material);
        this.scene.add(this.orb);
        
        // Inner glow sphere
        const innerGeometry = new THREE.SphereGeometry(4.5, 32, 32);
        const innerMaterial = new THREE.MeshBasicMaterial({
            color: 0x6366f1,
            transparent: true,
            opacity: 0.3,
        });
        const innerOrb = new THREE.Mesh(innerGeometry, innerMaterial);
        this.scene.add(innerOrb);
        this.innerOrb = innerOrb;
    }
    
    createParticles() {
        const particleCount = 200;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);
        const sizes = new Float32Array(particleCount);
        
        const colorOptions = [
            new THREE.Color(0x6366f1),
            new THREE.Color(0x8b5cf6),
            new THREE.Color(0x06b6d4),
            new THREE.Color(0x22d3ee),
        ];
        
        for (let i = 0; i < particleCount; i++) {
            const i3 = i * 3;
            
            // Position in spherical distribution
            const radius = 6 + Math.random() * 10;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            
            positions[i3] = radius * Math.sin(phi) * Math.cos(theta);
            positions[i3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
            positions[i3 + 2] = radius * Math.cos(phi);
            
            // Random color
            const color = colorOptions[Math.floor(Math.random() * colorOptions.length)];
            colors[i3] = color.r;
            colors[i3 + 1] = color.g;
            colors[i3 + 2] = color.b;
            
            sizes[i] = Math.random() * 3 + 1;
            
            this.particles.push({
                originalY: positions[i3 + 1],
                speed: Math.random() * 0.5 + 0.5,
                amplitude: Math.random() * 2 + 1,
            });
        }
        
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
        
        const material = new THREE.ShaderMaterial({
            uniforms: {
                time: { value: 0 },
                pixelRatio: { value: this.renderer.getPixelRatio() },
            },
            vertexShader: `
                attribute float size;
                attribute vec3 color;
                varying vec3 vColor;
                uniform float time;
                uniform float pixelRatio;
                
                void main() {
                    vColor = color;
                    vec3 pos = position;
                    
                    // Orbital movement
                    float angle = time * 0.2 + position.x * 0.1;
                    pos.x = cos(angle) * position.x - sin(angle) * position.z;
                    pos.z = sin(angle) * position.x + cos(angle) * position.z;
                    
                    vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
                    gl_PointSize = size * pixelRatio * (300.0 / -mvPosition.z);
                    gl_Position = projectionMatrix * mvPosition;
                }
            `,
            fragmentShader: `
                varying vec3 vColor;
                
                void main() {
                    float dist = length(gl_PointCoord - vec2(0.5));
                    if (dist > 0.5) discard;
                    
                    float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
                    gl_FragColor = vec4(vColor, alpha);
                }
            `,
            transparent: true,
            vertexColors: true,
            blending: THREE.AdditiveBlending,
            depthWrite: false,
        });
        
        this.particleSystem = new THREE.Points(geometry, material);
        this.scene.add(this.particleSystem);
    }
    
    createConnections() {
        const lineCount = 50;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(lineCount * 2 * 3);
        
        for (let i = 0; i < lineCount; i++) {
            const i6 = i * 6;
            const radius = 8 + Math.random() * 5;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            
            positions[i6] = radius * Math.sin(phi) * Math.cos(theta);
            positions[i6 + 1] = radius * Math.sin(phi) * Math.sin(theta);
            positions[i6 + 2] = radius * Math.cos(phi);
            
            const theta2 = theta + Math.random() * 0.5;
            const phi2 = phi + Math.random() * 0.5;
            
            positions[i6 + 3] = radius * Math.sin(phi2) * Math.cos(theta2);
            positions[i6 + 4] = radius * Math.sin(phi2) * Math.sin(theta2);
            positions[i6 + 5] = radius * Math.cos(phi2);
        }
        
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        
        const material = new THREE.LineBasicMaterial({
            color: 0x6366f1,
            transparent: true,
            opacity: 0.2,
            blending: THREE.AdditiveBlending,
        });
        
        this.connectionLines = new THREE.LineSegments(geometry, material);
        this.scene.add(this.connectionLines);
    }
    
    update(delta, elapsed) {
        this.time = elapsed;
        
        // Update orb shader
        if (this.orb && this.orb.material.uniforms) {
            this.orb.material.uniforms.time.value = elapsed;
        }
        
        // Update particle system
        if (this.particleSystem && this.particleSystem.material.uniforms) {
            this.particleSystem.material.uniforms.time.value = elapsed;
        }
        
        // Rotate orb
        if (this.orb) {
            this.orb.rotation.x = elapsed * 0.1;
            this.orb.rotation.y = elapsed * 0.15;
        }
        
        if (this.innerOrb) {
            this.innerOrb.rotation.x = -elapsed * 0.15;
            this.innerOrb.rotation.y = -elapsed * 0.1;
        }
        
        // Mouse interaction
        this.raycaster.setFromCamera(this.mouse, this.camera);
        
        // Subtle camera movement based on mouse
        this.camera.position.x += (this.mouse.x * 3 - this.camera.position.x) * 0.05;
        this.camera.position.y += (this.mouse.y * 3 - this.camera.position.y) * 0.05;
        this.camera.lookAt(0, 0, 0);
    }
}

/* =====================================================
   NEURAL NETWORK - Interactive Connections
   ===================================================== */
class NeuralNetwork extends ThreeScene {
    constructor(container) {
        super(container);
        this.nodes = [];
        this.links = [];
        this.nodeCount = 40;
    }
    
    setupScene() {
        super.setupScene();
        this.createNodes();
        this.createLinks();
    }
    
    createNodes() {
        const geometry = new THREE.SphereGeometry(0.3, 16, 16);
        
        for (let i = 0; i < this.nodeCount; i++) {
            const material = new THREE.MeshBasicMaterial({
                color: new THREE.Color().setHSL(0.7 + Math.random() * 0.2, 0.8, 0.6),
                transparent: true,
                opacity: 0.8,
            });
            
            const node = new THREE.Mesh(geometry, material);
            
            // Random position in space
            node.position.set(
                (Math.random() - 0.5) * 40,
                (Math.random() - 0.5) * 30,
                (Math.random() - 0.5) * 20
            );
            
            // Node data for animation
            node.userData = {
                originalPosition: node.position.clone(),
                speed: Math.random() * 0.5 + 0.5,
                amplitude: Math.random() * 2 + 1,
                phase: Math.random() * Math.PI * 2,
            };
            
            this.scene.add(node);
            this.nodes.push(node);
        }
    }
    
    createLinks() {
        const maxDistance = 12;
        
        for (let i = 0; i < this.nodes.length; i++) {
            for (let j = i + 1; j < this.nodes.length; j++) {
                const distance = this.nodes[i].position.distanceTo(this.nodes[j].position);
                
                if (distance < maxDistance) {
                    const points = [
                        this.nodes[i].position.clone(),
                        this.nodes[j].position.clone()
                    ];
                    
                    const geometry = new THREE.BufferGeometry().setFromPoints(points);
                    const material = new THREE.LineBasicMaterial({
                        color: 0x6366f1,
                        transparent: true,
                        opacity: 0.3 * (1 - distance / maxDistance),
                    });
                    
                    const line = new THREE.Line(geometry, material);
                    this.scene.add(line);
                    this.links.push({
                        line,
                        nodeA: i,
                        nodeB: j,
                    });
                }
            }
        }
    }
    
    update(delta, elapsed) {
        // Animate nodes
        this.nodes.forEach((node, index) => {
            const data = node.userData;
            
            // Floating animation
            node.position.y = data.originalPosition.y + 
                             Math.sin(elapsed * data.speed + data.phase) * data.amplitude;
            
            // Subtle movement
            node.position.x = data.originalPosition.x + 
                             Math.cos(elapsed * data.speed * 0.5 + data.phase) * data.amplitude * 0.5;
        });
        
        // Update links
        this.links.forEach((link) => {
            const points = [
                this.nodes[link.nodeA].position,
                this.nodes[link.nodeB].position
            ];
            link.line.geometry.setFromPoints(points);
        });
        
        // Mouse interaction - nodes react to cursor
        this.raycaster.setFromCamera(this.mouse, this.camera);
        const intersects = this.raycaster.intersectObjects(this.nodes);
        
        this.nodes.forEach((node) => {
            node.scale.setScalar(1);
            node.material.opacity = 0.8;
        });
        
        if (intersects.length > 0) {
            const hoveredNode = intersects[0].object;
            hoveredNode.scale.setScalar(1.5);
            hoveredNode.material.opacity = 1;
            
            // Highlight connected nodes
            this.links.forEach((link) => {
                if (link.nodeA === this.nodes.indexOf(hoveredNode) ||
                    link.nodeB === this.nodes.indexOf(hoveredNode)) {
                    link.line.material.opacity = 0.8;
                }
            });
        }
        
        // Camera follows mouse slightly
        this.camera.position.x += (this.mouse.x * 5 - this.camera.position.x) * 0.02;
        this.camera.position.y += (this.mouse.y * 5 - this.camera.position.y) * 0.02;
        this.camera.lookAt(0, 0, 0);
    }
}

/* =====================================================
   AGENTIC AI VISUALIZATION - Moving Nodes
   ===================================================== */
class AgenticVisualization extends ThreeScene {
    constructor(container) {
        super(container);
        this.agents = [];
        this.agentCount = 15;
        this.messages = [];
    }
    
    setupScene() {
        super.setupScene();
        this.createAgents();
        this.createMessageParticles();
    }
    
    createAgents() {
        const agentGeometry = new THREE.OctahedronGeometry(0.5, 0);
        
        for (let i = 0; i < this.agentCount; i++) {
            const hue = Math.random();
            const material = new THREE.MeshBasicMaterial({
                color: new THREE.Color().setHSL(0.6 + hue * 0.2, 0.9, 0.6),
                transparent: true,
                opacity: 0.9,
            });
            
            const agent = new THREE.Mesh(agentGeometry, material);
            
            // Start positions
            agent.position.set(
                (Math.random() - 0.5) * 30,
                (Math.random() - 0.5) * 20,
                (Math.random() - 0.5) * 15
            );
            
            agent.userData = {
                velocity: new THREE.Vector3(
                    (Math.random() - 0.5) * 0.1,
                    (Math.random() - 0.5) * 0.1,
                    (Math.random() - 0.5) * 0.1
                ),
                target: null,
                color: material.color.clone(),
            };
            
            this.scene.add(agent);
            this.agents.push(agent);
            
            // Create glow
            const glowGeometry = new THREE.SphereGeometry(1, 16, 16);
            const glowMaterial = new THREE.MeshBasicMaterial({
                color: material.color,
                transparent: true,
                opacity: 0.2,
            });
            const glow = new THREE.Mesh(glowGeometry, glowMaterial);
            agent.add(glow);
        }
    }
    
    createMessageParticles() {
        const particleCount = 100;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);
        
        for (let i = 0; i < particleCount; i++) {
            const i3 = i * 3;
            positions[i3] = (Math.random() - 0.5) * 40;
            positions[i3 + 1] = (Math.random() - 0.5) * 30;
            positions[i3 + 2] = (Math.random() - 0.5) * 20;
            
            colors[i3] = 0.4;
            colors[i3 + 1] = 0.5;
            colors[i3 + 2] = 0.95;
        }
        
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        
        const material = new THREE.PointsMaterial({
            size: 0.1,
            vertexColors: true,
            transparent: true,
            opacity: 0.6,
            blending: THREE.AdditiveBlending,
        });
        
        this.messageParticles = new THREE.Points(geometry, material);
        this.scene.add(this.messageParticles);
    }
    
    update(delta, elapsed) {
        // Move agents
        this.agents.forEach((agent, index) => {
            // Update velocity with slight random changes
            agent.userData.velocity.x += (Math.random() - 0.5) * 0.01;
            agent.userData.velocity.y += (Math.random() - 0.5) * 0.01;
            agent.userData.velocity.z += (Math.random() - 0.5) * 0.01;
            
            // Limit velocity
            agent.userData.velocity.clampLength(0, 0.2);
            
            // Apply velocity
            agent.position.add(agent.userData.velocity);
            
            // Bounce off boundaries
            const bounds = { x: 15, y: 10, z: 10 };
            ['x', 'y', 'z'].forEach((axis) => {
                if (Math.abs(agent.position[axis]) > bounds[axis]) {
                    agent.userData.velocity[axis] *= -1;
                    agent.position[axis] = Math.sign(agent.position[axis]) * bounds[axis];
                }
            });
            
            // Rotate agent
            agent.rotation.x += 0.02;
            agent.rotation.y += 0.03;
            
            // Pulse effect
            const scale = 1 + Math.sin(elapsed * 3 + index) * 0.2;
            agent.scale.setScalar(scale);
        });
        
        // Occasionally send "messages" between agents
        if (Math.random() < 0.02 && this.agents.length > 1) {
            const agentA = this.agents[Math.floor(Math.random() * this.agents.length)];
            const agentB = this.agents[Math.floor(Math.random() * this.agents.length)];
            
            if (agentA !== agentB) {
                this.sendMessage(agentA, agentB);
            }
        }
        
        // Update message particles
        if (this.messageParticles) {
            this.messageParticles.rotation.y = elapsed * 0.05;
        }
        
        // Camera movement
        this.camera.position.x = Math.sin(elapsed * 0.1) * 3;
        this.camera.position.z = 25 + Math.cos(elapsed * 0.1) * 3;
        this.camera.lookAt(0, 0, 0);
    }
    
    sendMessage(from, to) {
        // Create a visual message trail
        const points = [from.position.clone(), to.position.clone()];
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const material = new THREE.LineBasicMaterial({
            color: from.userData.color,
            transparent: true,
            opacity: 0.8,
        });
        
        const message = new THREE.Line(geometry, material);
        this.scene.add(message);
        
        // Fade out and remove
        const fadeMessage = () => {
            message.material.opacity -= 0.02;
            if (message.material.opacity <= 0) {
                this.scene.remove(message);
                geometry.dispose();
                material.dispose();
            } else {
                requestAnimationFrame(fadeMessage);
            }
        };
        fadeMessage();
    }
}

/* =====================================================
   DATA UNIVERSE - Knowledge Graph
   ===================================================== */
class DataUniverse extends ThreeScene {
    constructor(container) {
        super(container);
        this.dataPoints = [];
        this.clusters = [];
    }
    
    setupScene() {
        super.setupScene();
        this.createClusters();
        this.createDataPoints();
        this.createConnections();
    }
    
    createClusters() {
        const clusterCount = 5;
        const clusterColors = [
            0x6366f1, 0x8b5cf6, 0x06b6d4, 0x10b981, 0xf59e0b
        ];
        
        for (let i = 0; i < clusterCount; i++) {
            const geometry = new THREE.SphereGeometry(2, 32, 32);
            const material = new THREE.MeshBasicMaterial({
                color: clusterColors[i],
                transparent: true,
                opacity: 0.1,
                wireframe: true,
            });
            
            const cluster = new THREE.Mesh(geometry, material);
            cluster.position.set(
                (Math.random() - 0.5) * 30,
                (Math.random() - 0.5) * 20,
                (Math.random() - 0.5) * 15
            );
            
            cluster.userData = {
                rotationSpeed: (Math.random() - 0.5) * 0.02,
            };
            
            this.scene.add(cluster);
            this.clusters.push(cluster);
        }
    }
    
    createDataPoints() {
        const pointCount = 300;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(pointCount * 3);
        const colors = new Float32Array(pointCount * 3);
        
        for (let i = 0; i < pointCount; i++) {
            const i3 = i * 3;
            
            // Distribute around clusters
            const clusterIndex = Math.floor(Math.random() * this.clusters.length);
            const cluster = this.clusters[clusterIndex];
            
            const spread = 3;
            positions[i3] = cluster.position.x + (Math.random() - 0.5) * spread;
            positions[i3 + 1] = cluster.position.y + (Math.random() - 0.5) * spread;
            positions[i3 + 2] = cluster.position.z + (Math.random() - 0.5) * spread;
            
            // Color based on cluster
            const color = new THREE.Color(this.clusters[clusterIndex].material.color);
            colors[i3] = color.r;
            colors[i3 + 1] = color.g;
            colors[i3 + 2] = color.b;
            
            this.dataPoints.push({
                clusterIndex,
                originalPosition: new THREE.Vector3(positions[i3], positions[i3 + 1], positions[i3 + 2]),
            });
        }
        
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        
        const material = new THREE.PointsMaterial({
            size: 0.15,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            blending: THREE.AdditiveBlending,
        });
        
        this.dataPointSystem = new THREE.Points(geometry, material);
        this.scene.add(this.dataPointSystem);
    }
    
    createConnections() {
        // Create some connection lines between nearby points
        const positions = this.dataPointSystem.geometry.attributes.position.array;
        
        for (let i = 0; i < 30; i++) {
            const idx1 = Math.floor(Math.random() * this.dataPoints.length);
            const idx2 = Math.floor(Math.random() * this.dataPoints.length);
            
            if (idx1 !== idx2) {
                const points = [
                    new THREE.Vector3(
                        positions[idx1 * 3],
                        positions[idx1 * 3 + 1],
                        positions[idx1 * 3 + 2]
                    ),
                    new THREE.Vector3(
                        positions[idx2 * 3],
                        positions[idx2 * 3 + 1],
                        positions[idx2 * 3 + 2]
                    )
                ];
                
                const geometry = new THREE.BufferGeometry().setFromPoints(points);
                const material = new THREE.LineBasicMaterial({
                    color: 0x6366f1,
                    transparent: true,
                    opacity: 0.2,
                });
                
                const line = new THREE.Line(geometry, material);
                this.scene.add(line);
            }
        }
    }
    
    update(delta, elapsed) {
        // Rotate clusters
        this.clusters.forEach((cluster) => {
            cluster.rotation.x += cluster.userData.rotationSpeed;
            cluster.rotation.y += cluster.userData.rotationSpeed * 1.5;
        });
        
        // Slowly rotate entire scene
        this.dataPointSystem.rotation.y = elapsed * 0.03;
        
        // Mouse interaction - attract points slightly
        const positions = this.dataPointSystem.geometry.attributes.position.array;
        
        for (let i = 0; i < this.dataPoints.length; i++) {
            const i3 = i * 3;
            const point = this.dataPoints[i];
            const original = point.originalPosition;
            
            // Gentle floating motion
            const offsetX = Math.sin(elapsed * 0.5 + i * 0.1) * 0.1;
            const offsetY = Math.cos(elapsed * 0.3 + i * 0.2) * 0.1;
            
            positions[i3] = original.x + offsetX;
            positions[i3 + 1] = original.y + offsetY;
            positions[i3 + 2] = original.z;
        }
        
        this.dataPointSystem.geometry.attributes.position.needsUpdate = true;
        
        // Camera orbit
        this.camera.position.x = Math.sin(elapsed * 0.1) * 30;
        this.camera.position.z = Math.cos(elapsed * 0.1) * 30;
        this.camera.lookAt(0, 0, 0);
    }
}

// =====================================================
// INITIALIZE 3D SCENES
// =====================================================
document.addEventListener('DOMContentLoaded', () => {
    // AI Orb for hero section
    const orbContainer = document.getElementById('ai-orb-container');
    if (orbContainer && typeof THREE !== 'undefined') {
        const aiOrb = new AIOrb(orbContainer);
        window.aiOrb = aiOrb;
    }
    
    // Neural Network for ecosystem section
    const neuralContainer = document.getElementById('neural-network-container');
    if (neuralContainer && typeof THREE !== 'undefined') {
        const neuralNetwork = new NeuralNetwork(neuralContainer);
        window.neuralNetwork = neuralNetwork;
    }
    
    // Agentic Visualization
    const agenticContainer = document.getElementById('agentic-container');
    if (agenticContainer && typeof THREE !== 'undefined') {
        const agenticViz = new AgenticVisualization(agenticContainer);
        window.agenticViz = agenticViz;
    }
    
    // Data Universe for research section
    const universeContainer = document.getElementById('data-universe-container');
    if (universeContainer && typeof THREE !== 'undefined') {
        const dataUniverse = new DataUniverse(universeContainer);
        window.dataUniverse = dataUniverse;
    }
    
    // Pause/resume based on visibility
    document.addEventListener('visibilitychange', () => {
        const scenes = [window.aiOrb, window.neuralNetwork, window.agenticViz, window.dataUniverse];
        scenes.forEach((scene) => {
            if (scene) {
                if (document.hidden) {
                    scene.renderer.setAnimationLoop(null);
                } else {
                    scene.renderer.setAnimationLoop(scene.animate.bind(scene));
                }
            }
        });
    });
});