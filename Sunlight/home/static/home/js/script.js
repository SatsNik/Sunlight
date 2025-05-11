// Main JavaScript for Sunlight Energy Trading Platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme based on stored preference or default to dark
    initTheme();
    
    // Setup theme toggle functionality
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Smooth scrolling for navigation links
    const links = document.querySelectorAll('a[href^="#"]');
    
    for (const link of links) {
        link.addEventListener('click', smoothScroll);
    }
    
    function smoothScroll(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
    
    // Add animation class to elements when they become visible
    const animatedElements = document.querySelectorAll('.tech-item, .profile-img, .intro-box, .welcome-heading');
    
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Add a small delay for a cascade effect
                    setTimeout(() => {
                        entry.target.classList.add('animate');
                    }, Math.random() * 300);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });
        
        animatedElements.forEach(item => {
            observer.observe(item);
        });
    }
    
    // Create dynamic blockchain network elements
    createBlockchainNetwork();
    
    // Create subtle blockchain-inspired floating particles
    createParticles();
});

// Function to create floating particles
function createParticles() {
    const heroSection = document.querySelector('.hero');
    const numParticles = 15;
    
    // Only create particles if hero section exists
    if (!heroSection) return;
    
    // Create a container for the particles
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles-container';
    particlesContainer.style.position = 'absolute';
    particlesContainer.style.top = '0';
    particlesContainer.style.left = '0';
    particlesContainer.style.width = '100%';
    particlesContainer.style.height = '100%';
    particlesContainer.style.overflow = 'hidden';
    particlesContainer.style.zIndex = '-1';
    
    heroSection.style.position = 'relative';
    heroSection.appendChild(particlesContainer);
    
    // Create the particles
    for (let i = 0; i < numParticles; i++) {
        createParticle(particlesContainer);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    
    // Randomly choose particle type (circle, hexagon, square)
    const particleTypes = ['circle', 'hexagon', 'square'];
    const particleType = particleTypes[Math.floor(Math.random() * particleTypes.length)];
    
    // Set basic styles
    particle.style.position = 'absolute';
    particle.style.opacity = (Math.random() * 0.2 + 0.1).toString();
    
    // Size between 5px and 20px
    const size = Math.random() * 15 + 5;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    
    // Random position
    particle.style.top = `${Math.random() * 100}%`;
    particle.style.left = `${Math.random() * 100}%`;
    
    // Set color - choose between blockchain, solar, eco colors
    const colors = [
        'rgba(139, 92, 246, 0.5)',  // Blockchain purple
        'rgba(59, 130, 246, 0.5)',   // Blue
        'rgba(16, 185, 129, 0.5)',   // Eco green
        'rgba(251, 191, 36, 0.5)'    // Solar yellow
    ];
    const color = colors[Math.floor(Math.random() * colors.length)];
    
    // Apply different shapes
    if (particleType === 'circle') {
        particle.style.borderRadius = '50%';
        particle.style.background = color;
    } else if (particleType === 'hexagon') {
        particle.style.width = '0';
        particle.style.height = '0';
        particle.style.borderLeft = `${size/2}px solid transparent`;
        particle.style.borderRight = `${size/2}px solid transparent`;
        particle.style.borderBottom = `${size}px solid ${color}`;
    } else {
        // Square
        particle.style.background = color;
        particle.style.transform = `rotate(${Math.random() * 45}deg)`;
    }
    
    // Animation duration between 30s and 60s
    const duration = Math.random() * 30 + 30;
    
    // Create and apply the keyframe animation
    particle.style.animation = `float ${duration}s linear infinite`;
    
    // Add to container
    container.appendChild(particle);
    
    // Create the floating animation if it doesn't exist
    if (!document.querySelector('#particle-animation')) {
        const style = document.createElement('style');
        style.id = 'particle-animation';
        style.textContent = `
            @keyframes float {
                0% {
                    transform: translate(0, 0) rotate(0);
                }
                25% {
                    transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) rotate(${Math.random() * 180}deg);
                }
                50% {
                    transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) rotate(${Math.random() * 360}deg);
                }
                75% {
                    transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) rotate(${Math.random() * 540}deg);
                }
                100% {
                    transform: translate(0, 0) rotate(720deg);
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Theme management functions
function initTheme() {
    // Check for saved theme preference, default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setTheme(savedTheme);
}

function setTheme(theme) {
    if (theme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
    } else {
        document.documentElement.removeAttribute('data-theme');
    }
    
    // Save theme preference
    localStorage.setItem('theme', theme);
}

function toggleTheme() {
    // Get current theme
    const currentTheme = localStorage.getItem('theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    // Show transition animation
    if (newTheme === 'light') {
        showLightThemeTransition();
    } else {
        showDarkThemeTransition();
    }
    
    // Apply theme after a small delay for animation
    setTimeout(() => {
        setTheme(newTheme);
    }, 300);
}

// Animation for transitioning to light (eco-friendly) theme
function showLightThemeTransition() {
    const transitionEl = document.querySelector('.theme-transition');
    const sunRays = document.querySelector('.sun-rays');
    const leaves = document.querySelector('.leaves');
    const networkContainer = document.querySelector('.blockchain-network');
    
    if (!transitionEl || !sunRays || !leaves) return;
    
    // Clear any existing leaves
    leaves.innerHTML = '';
    
    // Create new leaves
    for (let i = 0; i < 15; i++) {
        createLeaf(leaves);
    }
    
    // Softly hide network visualization for the transition
    if (networkContainer) {
        networkContainer.style.transition = 'opacity 0.5s ease';
        networkContainer.style.opacity = '0.2';
    }
    
    // Activate transition elements
    transitionEl.classList.add('active');
    sunRays.classList.add('active');
    
    // After sun rays expand, show leaves
    setTimeout(() => {
        leaves.classList.add('active');
    }, 500);
    
    // Hide transition after animation completes
    setTimeout(() => {
        transitionEl.classList.remove('active');
        sunRays.classList.remove('active');
        leaves.classList.remove('active');
        
        // Restore network visualization with eco-friendly styling
        if (networkContainer) {
            setTimeout(() => {
                networkContainer.style.opacity = '1';
                // Update network connections with eco-friendly colors
                const svg = networkContainer.querySelector('svg');
                const nodes = Array.from(networkContainer.querySelectorAll('.network-node'));
                if (svg && nodes.length > 0) {
                    updateNetworkConnections(svg, nodes);
                }
            }, 500);
        }
    }, 2000);
}

// Animation for transitioning to dark theme
function showDarkThemeTransition() {
    const transitionEl = document.querySelector('.theme-transition');
    const sunRays = document.querySelector('.sun-rays');
    const leaves = document.querySelector('.leaves');
    const networkContainer = document.querySelector('.blockchain-network');
    
    if (!transitionEl || !sunRays || !leaves) return;
    
    // Softly hide network visualization for the transition
    if (networkContainer) {
        networkContainer.style.transition = 'opacity 0.5s ease';
        networkContainer.style.opacity = '0.2';
    }
    
    // Fade out any content
    transitionEl.classList.add('active');
    
    // Hide transition after animation completes
    setTimeout(() => {
        transitionEl.classList.remove('active');
        
        // Restore network visualization with blockchain styling
        if (networkContainer) {
            setTimeout(() => {
                networkContainer.style.opacity = '1';
                // Update network connections with blockchain-themed colors
                const svg = networkContainer.querySelector('svg');
                const nodes = Array.from(networkContainer.querySelectorAll('.network-node'));
                if (svg && nodes.length > 0) {
                    updateNetworkConnections(svg, nodes);
                }
            }, 500);
        }
    }, 1000);
}

// Function to create the blockchain network visualization
function createBlockchainNetwork() {
    const networkContainer = document.querySelector('.blockchain-network');
    const networkNodesContainer = document.querySelector('.network-nodes');
    
    if (!networkContainer || !networkNodesContainer) return;
    
    // Clear any existing nodes
    networkNodesContainer.innerHTML = '';
    
    // Create SVG for network connections
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', '100%');
    svg.style.position = 'absolute';
    svg.style.top = '0';
    svg.style.left = '0';
    svg.style.zIndex = '0';
    svg.style.opacity = '0.2';
    
    // Add to container before nodes so it appears behind them
    networkContainer.insertBefore(svg, networkNodesContainer);
    
    // Create blockchain nodes (15-20 nodes)
    const numNodes = Math.floor(Math.random() * 6) + 15;
    const nodes = [];
    
    for (let i = 0; i < numNodes; i++) {
        const node = createNetworkNode(networkNodesContainer);
        nodes.push(node);
    }
    
    // Create connections between nodes
    setTimeout(() => {
        createNetworkConnections(svg, nodes);
    }, 500);
    
    // Periodically update the connections to create a living network effect
    setInterval(() => {
        updateNetworkConnections(svg, nodes);
    }, 8000);
}

// Create a blockchain network node
function createNetworkNode(container) {
    const node = document.createElement('div');
    node.className = 'network-node';
    
    // Set node appearance
    node.style.position = 'absolute';
    node.style.width = '8px';
    node.style.height = '8px';
    node.style.borderRadius = '50%';
    
    // Random position (with padding from edges)
    const posX = 5 + Math.random() * 90; // 5-95%
    const posY = 5 + Math.random() * 90; // 5-95%
    node.style.top = `${posY}%`;
    node.style.left = `${posX}%`;
    
    // Color based on type of node
    const nodeTypes = ['blockchain', 'solar', 'eco', 'blockchain']; // More blockchain nodes
    const nodeType = nodeTypes[Math.floor(Math.random() * nodeTypes.length)];
    
    // Set color based on node type
    if (nodeType === 'blockchain') {
        node.style.background = 'rgba(139, 92, 246, 0.8)';
        node.style.boxShadow = '0 0 10px rgba(139, 92, 246, 0.6)';
    } else if (nodeType === 'solar') {
        node.style.background = 'rgba(251, 191, 36, 0.8)';
        node.style.boxShadow = '0 0 10px rgba(251, 191, 36, 0.6)';
    } else {
        node.style.background = 'rgba(16, 185, 129, 0.8)';
        node.style.boxShadow = '0 0 10px rgba(16, 185, 129, 0.6)';
    }
    
    // Pulse animation
    node.style.animation = `nodePulse ${Math.random() * 2 + 2}s infinite alternate`;
    
    // Store node type and position for connection drawing
    node.dataset.type = nodeType;
    node.dataset.x = posX;
    node.dataset.y = posY;
    
    // Add to container
    container.appendChild(node);
    
    // Create pulse animation if it doesn't exist
    if (!document.querySelector('#node-pulse-animation')) {
        const style = document.createElement('style');
        style.id = 'node-pulse-animation';
        style.textContent = `
            @keyframes nodePulse {
                0% { transform: scale(0.8); opacity: 0.6; }
                100% { transform: scale(1.2); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }
    
    return node;
}

// Create connections between network nodes
function createNetworkConnections(svg, nodes) {
    // Clear any existing connections
    svg.innerHTML = '';
    
    // Connect each node to 2-4 nearby nodes
    nodes.forEach(node => {
        const numConnections = Math.floor(Math.random() * 3) + 2;
        const nodeType = node.dataset.type;
        const x1 = parseFloat(node.dataset.x);
        const y1 = parseFloat(node.dataset.y);
        
        // Sort nodes by distance to current node
        const sortedNodes = [...nodes]
            .filter(n => n !== node) // Don't connect to self
            .map(n => {
                const x2 = parseFloat(n.dataset.x);
                const y2 = parseFloat(n.dataset.y);
                const distance = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
                return { node: n, distance };
            })
            .sort((a, b) => a.distance - b.distance);
        
        // Connect to closest nodes
        for (let i = 0; i < Math.min(numConnections, sortedNodes.length); i++) {
            const targetNode = sortedNodes[i].node;
            const x2 = parseFloat(targetNode.dataset.x);
            const y2 = parseFloat(targetNode.dataset.y);
            
            // Create line
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', x1 + '%');
            line.setAttribute('y1', y1 + '%');
            line.setAttribute('x2', x2 + '%');
            line.setAttribute('y2', y2 + '%');
            
            // Style based on node types
            if (nodeType === 'blockchain' || targetNode.dataset.type === 'blockchain') {
                line.setAttribute('stroke', 'rgba(139, 92, 246, 0.4)');
            } else if (nodeType === 'solar' || targetNode.dataset.type === 'solar') {
                line.setAttribute('stroke', 'rgba(251, 191, 36, 0.4)');
            } else {
                line.setAttribute('stroke', 'rgba(16, 185, 129, 0.4)');
            }
            
            line.setAttribute('stroke-width', '1');
            line.setAttribute('stroke-dasharray', '2,2');
            line.classList.add('network-connection');
            
            // Data flow animation
            const animationDuration = Math.random() * 8 + 12;
            line.style.animation = `dataFlow ${animationDuration}s linear infinite`;
            
            svg.appendChild(line);
        }
    });
    
    // Create data flow animation if it doesn't exist
    if (!document.querySelector('#data-flow-animation')) {
        const style = document.createElement('style');
        style.id = 'data-flow-animation';
        style.textContent = `
            @keyframes dataFlow {
                0% { stroke-dashoffset: 0; }
                100% { stroke-dashoffset: 1000; }
            }
        `;
        document.head.appendChild(style);
    }
}

// Update network connections to simulate a living network
function updateNetworkConnections(svg, nodes) {
    // Fade out current connections
    const connections = svg.querySelectorAll('.network-connection');
    connections.forEach(connection => {
        connection.style.transition = 'opacity 1s ease';
        connection.style.opacity = '0';
    });
    
    // Create new connections after fade out
    setTimeout(() => {
        createNetworkConnections(svg, nodes);
    }, 1000);
}

// Function to create animated leaves
function createLeaf(container) {
    const leaf = document.createElement('div');
    leaf.className = 'leaf';
    
    // Randomize leaf properties
    const size = Math.random() * 15 + 10; // Size between 10px and 25px
    leaf.style.width = `${size}px`;
    leaf.style.height = `${size}px`;
    
    // Random position
    leaf.style.top = `${Math.random() * 100}%`;
    leaf.style.left = `${Math.random() * 100}%`;
    
    // Random rotation
    leaf.style.transform = `rotate(${Math.random() * 360}deg)`;
    
    // Add falling animation
    const fallDuration = Math.random() * 5 + 3; // Between 3-8 seconds
    leaf.style.animation = `fall ${fallDuration}s ease-in-out forwards`;
    
    // Add to container
    container.appendChild(leaf);
    
    // Create falling animation if it doesn't exist
    if (!document.querySelector('#leaf-animation')) {
        const style = document.createElement('style');
        style.id = 'leaf-animation';
        style.textContent = `
            @keyframes fall {
                0% {
                    transform: translate(0, -100%) rotate(0deg);
                    opacity: 0;
                }
                10% {
                    opacity: 1;
                }
                100% {
                    transform: translate(${Math.random() * 200 - 100}px, ${window.innerHeight}px) rotate(${Math.random() * 720}deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}