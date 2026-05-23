// ============================================================
// NeuralTrade AI - 3D Particle Stock Chart Background
// Developed by issu321
// https://github.com/issu321/Stock-Price-Prediction-Using-Machine-Learning
// ============================================================

(function() {
    const canvas = document.getElementById('three-canvas');
    if (!canvas) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Generate stock-like price data for particles
    const particleCount = 800;
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    const sizes = new Float32Array(particleCount);
    const speeds = new Float32Array(particleCount);

    const color1 = new THREE.Color(0x00f0ff);
    const color2 = new THREE.Color(0xa78bfa);
    const color3 = new THREE.Color(0x34d399);

    for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;
        // Create a wave-like stock chart pattern
        const x = (i / particleCount) * 40 - 20;
        const wave = Math.sin(x * 0.5) * 3 + Math.sin(x * 1.2) * 1.5 + Math.cos(x * 0.3) * 2;
        const y = wave + (Math.random() - 0.5) * 4;
        const z = (Math.random() - 0.5) * 15;

        positions[i3] = x;
        positions[i3 + 1] = y;
        positions[i3 + 2] = z;

        // Mix colors
        const mixFactor = Math.random();
        let c;
        if (mixFactor < 0.33) {
            c = color1.clone().lerp(color2, Math.random());
        } else if (mixFactor < 0.66) {
            c = color2.clone().lerp(color3, Math.random());
        } else {
            c = color3.clone().lerp(color1, Math.random());
        }
        colors[i3] = c.r;
        colors[i3 + 1] = c.g;
        colors[i3 + 2] = c.b;

        sizes[i] = Math.random() * 3 + 1;
        speeds[i] = Math.random() * 0.02 + 0.005;
    }

    // Particle geometry
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    // Custom shader material for glowing particles
    const material = new THREE.ShaderMaterial({
        uniforms: {
            uTime: { value: 0 },
            uPixelRatio: { value: Math.min(window.devicePixelRatio, 2) }
        },
        vertexShader: `
            attribute float size;
            attribute vec3 color;
            varying vec3 vColor;
            uniform float uTime;
            uniform float uPixelRatio;

            void main() {
                vColor = color;
                vec3 pos = position;
                pos.y += sin(uTime * 0.5 + position.x * 0.3) * 0.5;
                pos.z += cos(uTime * 0.3 + position.y * 0.2) * 0.3;
                vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
                gl_PointSize = size * uPixelRatio * (300.0 / -mvPosition.z);
                gl_Position = projectionMatrix * mvPosition;
            }
        `,
        fragmentShader: `
            varying vec3 vColor;

            void main() {
                float dist = length(gl_PointCoord - vec2(0.5));
                if (dist > 0.5) discard;
                float alpha = 1.0 - smoothstep(0.0, 0.5, dist);
                alpha *= 0.8;
                gl_FragColor = vec4(vColor, alpha);
            }
        `,
        transparent: true,
        depthWrite: false,
        blending: THREE.AdditiveBlending
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // Stock chart line
    const linePoints = [];
    for (let i = 0; i < 100; i++) {
        const x = (i / 100) * 30 - 15;
        const y = Math.sin(x * 0.4) * 2 + Math.cos(x * 0.8) * 1 + Math.sin(x * 1.5) * 0.5;
        linePoints.push(new THREE.Vector3(x, y, 0));
    }
    const lineGeometry = new THREE.BufferGeometry().setFromPoints(linePoints);
    const lineMaterial = new THREE.LineBasicMaterial({
        color: 0x00f0ff,
        transparent: true,
        opacity: 0.3
    });
    const line = new THREE.Line(lineGeometry, lineMaterial);
    scene.add(line);

    // Floating cubes (data blocks)
    const cubeGeometry = new THREE.BoxGeometry(0.3, 0.3, 0.3);
    const cubes = [];
    for (let i = 0; i < 30; i++) {
        const cubeMat = new THREE.MeshBasicMaterial({
            color: Math.random() > 0.5 ? 0x00f0ff : 0xa78bfa,
            transparent: true,
            opacity: 0.4,
            wireframe: true
        });
        const cube = new THREE.Mesh(cubeGeometry, cubeMat);
        cube.position.set(
            (Math.random() - 0.5) * 30,
            (Math.random() - 0.5) * 15,
            (Math.random() - 0.5) * 10
        );
        cube.userData = {
            rotSpeed: {
                x: (Math.random() - 0.5) * 0.02,
                y: (Math.random() - 0.5) * 0.02,
                z: (Math.random() - 0.5) * 0.02
            },
            floatSpeed: Math.random() * 0.01 + 0.005,
            floatOffset: Math.random() * Math.PI * 2
        };
        scene.add(cube);
        cubes.push(cube);
    }

    camera.position.z = 12;
    camera.position.y = 2;

    // Mouse interaction
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX / window.innerWidth) * 2 - 1;
        mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
    });

    // Animation loop
    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);
        const elapsedTime = clock.getElapsedTime();

        material.uniforms.uTime.value = elapsedTime;

        // Smooth camera follow mouse
        targetX = mouseX * 2;
        targetY = mouseY * 2;
        camera.position.x += (targetX - camera.position.x) * 0.02;
        camera.position.y += (targetY + 2 - camera.position.y) * 0.02;
        camera.lookAt(0, 0, 0);

        // Animate cubes
        cubes.forEach(cube => {
            cube.rotation.x += cube.userData.rotSpeed.x;
            cube.rotation.y += cube.userData.rotSpeed.y;
            cube.rotation.z += cube.userData.rotSpeed.z;
            cube.position.y += Math.sin(elapsedTime * cube.userData.floatSpeed + cube.userData.floatOffset) * 0.01;
        });

        // Slowly rotate line
        line.rotation.y = Math.sin(elapsedTime * 0.1) * 0.1;

        renderer.render(scene, camera);
    }

    animate();

    // Resize handler
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
        material.uniforms.uPixelRatio.value = Math.min(window.devicePixelRatio, 2);
    });
})();
