// ============================================================
// NeuralTrade AI Website - Main JavaScript
// Developed by issu321
// https://github.com/issu321/Stock-Price-Prediction-Using-Machine-Learning
// ============================================================

document.addEventListener('DOMContentLoaded', function() {

    // ============================================================
    // MOBILE MENU
    // ============================================================
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileBtn.textContent = navLinks.classList.contains('active') ? '✕' : '☰';
        });
    }

    // ============================================================
    // NAVBAR SCROLL EFFECT
    // ============================================================
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // ============================================================
    // SCROLL REVEAL ANIMATIONS
    // ============================================================
    const fadeElements = document.querySelectorAll('.fade-in');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    fadeElements.forEach(el => observer.observe(el));

    // ============================================================
    // 3D TILT CARDS
    // ============================================================
    const tiltCards = document.querySelectorAll('.tilt-card');

    tiltCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
        });
    });

    // ============================================================
    // TYPING EFFECT
    // ============================================================
    const typingElements = document.querySelectorAll('.typing-text');
    typingElements.forEach(el => {
        const text = el.getAttribute('data-text') || el.textContent;
        el.textContent = '';
        el.classList.add('typing-cursor');
        let i = 0;

        const type = () => {
            if (i < text.length) {
                el.textContent += text.charAt(i);
                i++;
                setTimeout(type, 50 + Math.random() * 50);
            }
        };

        setTimeout(type, 500);
    });

    // ============================================================
    // COUNTER ANIMATION
    // ============================================================
    const counters = document.querySelectorAll('.counter');

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'));
                const suffix = counter.getAttribute('data-suffix') || '';
                const duration = 2000;
                const step = target / (duration / 16);
                let current = 0;

                const update = () => {
                    current += step;
                    if (current < target) {
                        counter.textContent = Math.floor(current) + suffix;
                        requestAnimationFrame(update);
                    } else {
                        counter.textContent = target + suffix;
                    }
                };

                update();
                counterObserver.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(c => counterObserver.observe(c));

    // ============================================================
    // PROGRESS BAR ANIMATION
    // ============================================================
    const progressBars = document.querySelectorAll('.progress-bar-fill');

    const progressObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const width = bar.getAttribute('data-width');
                bar.style.width = width + '%';
                progressObserver.unobserve(bar);
            }
        });
    }, { threshold: 0.5 });

    progressBars.forEach(b => progressObserver.observe(b));

    // ============================================================
    // DEMO SIMULATION
    // ============================================================
    const demoTicker = document.getElementById('demo-ticker');
    const demoPeriod = document.getElementById('demo-period');
    const demoBtn = document.getElementById('demo-btn');
    const demoMetrics = document.getElementById('demo-metrics');
    const demoChart = document.getElementById('demo-chart');
    const demoPrediction = document.getElementById('demo-prediction');

    if (demoBtn && demoChart) {
        demoBtn.addEventListener('click', runDemoSimulation);
    }

    function runDemoSimulation() {
        const ticker = demoTicker ? demoTicker.value.toUpperCase() : 'AAPL';

        // Show loading
        demoBtn.innerHTML = '<span class="spinner">⚡</span> Analyzing...';
        demoBtn.disabled = true;

        // Simulate processing delay
        setTimeout(() => {
            // Generate demo data
            const data = generateDemoData(ticker);

            // Update metrics
            if (demoMetrics) {
                demoMetrics.innerHTML = `
                    <div class="demo-metric">
                        <div class="demo-metric-label">Current Price</div>
                        <div class="demo-metric-value">$${data.currentPrice.toFixed(2)}</div>
                    </div>
                    <div class="demo-metric">
                        <div class="demo-metric-label">Predicted</div>
                        <div class="demo-metric-value" style="color: var(--neon-green);">$${data.predictedPrice.toFixed(2)}</div>
                    </div>
                    <div class="demo-metric">
                        <div class="demo-metric-label">R² Score</div>
                        <div class="demo-metric-value">${data.r2Score.toFixed(4)}</div>
                    </div>
                    <div class="demo-metric">
                        <div class="demo-metric-label">Confidence</div>
                        <div class="demo-metric-value">${data.confidence}%</div>
                    </div>
                `;
            }

            // Draw chart
            drawDemoChart(demoChart, data);

            // Update prediction text
            if (demoPrediction) {
                const direction = data.predictedPrice > data.currentPrice ? 'rise' : 'fall';
                const color = direction === 'rise' ? 'var(--neon-green)' : 'var(--neon-red)';
                demoPrediction.innerHTML = `
                    <div class="info-box" style="margin-top: 1.5rem;">
                        <h4 style="color: var(--neon-cyan); margin-top: 0;">🧠 AI Analysis for ${ticker}</h4>
                        <p>ML models predict the price will likely <strong style="color: ${color};">${direction}</strong> 
                        from <strong>$${data.currentPrice.toFixed(2)}</strong> to approximately <strong>$${data.predictedPrice.toFixed(2)}</strong>.</p>
                        <p>Best model: <strong style="color: var(--neon-green);">${data.bestModel}</strong> with R² = ${data.r2Score.toFixed(4)}</p>
                    </div>
                `;
            }

            demoBtn.innerHTML = '🔄 Analyze Again';
            demoBtn.disabled = false;
        }, 1500);
    }

    function generateDemoData(ticker) {
        const basePrices = {
            'AAPL': 175.50, 'TSLA': 240.30, 'GOOGL': 138.20, 'AMZN': 178.90,
            'MSFT': 420.15, 'NVDA': 890.50, 'META': 505.20, 'NFLX': 625.40,
            'AMD': 165.80, 'INTC': 32.40
        };

        const base = basePrices[ticker] || (100 + Math.random() * 400);
        const change = (Math.random() - 0.4) * base * 0.05;

        return {
            ticker: ticker,
            currentPrice: base,
            predictedPrice: base + change,
            r2Score: 0.85 + Math.random() * 0.12,
            confidence: Math.floor(75 + Math.random() * 20),
            bestModel: ['Random Forest', 'Linear Regression', 'SVR'][Math.floor(Math.random() * 3)],
            history: Array.from({length: 60}, (_, i) => ({
                day: i,
                price: base * (1 + Math.sin(i * 0.1) * 0.08 + (Math.random() - 0.5) * 0.03)
            }))
        };
    }

    function drawDemoChart(container, data) {
        if (!container) return;

        const canvas = document.createElement('canvas');
        canvas.width = container.offsetWidth || 800;
        canvas.height = 350;
        container.innerHTML = '';
        container.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        const w = canvas.width;
        const h = canvas.height;
        const padding = 50;

        // Clear
        ctx.fillStyle = 'rgba(5, 5, 5, 0.3)';
        ctx.fillRect(0, 0, w, h);

        // Grid
        ctx.strokeStyle = 'rgba(0, 240, 255, 0.05)';
        ctx.lineWidth = 1;
        for (let i = 0; i <= 10; i++) {
            const y = padding + (h - 2 * padding) * (i / 10);
            ctx.beginPath();
            ctx.moveTo(padding, y);
            ctx.lineTo(w - padding, y);
            ctx.stroke();
        }

        // Find min/max
        const prices = data.history.map(d => d.price);
        const minP = Math.min(...prices) * 0.98;
        const maxP = Math.max(...prices) * 1.02;

        // Draw line
        ctx.strokeStyle = '#00f0ff';
        ctx.lineWidth = 2;
        ctx.shadowColor = '#00f0ff';
        ctx.shadowBlur = 10;
        ctx.beginPath();

        data.history.forEach((pt, i) => {
            const x = padding + (w - 2 * padding) * (i / (data.history.length - 1));
            const y = padding + (h - 2 * padding) * (1 - (pt.price - minP) / (maxP - minP));
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.stroke();
        ctx.shadowBlur = 0;

        // Fill area under line
        ctx.fillStyle = 'rgba(0, 240, 255, 0.08)';
        ctx.beginPath();
        ctx.moveTo(padding, h - padding);
        data.history.forEach((pt, i) => {
            const x = padding + (w - 2 * padding) * (i / (data.history.length - 1));
            const y = padding + (h - 2 * padding) * (1 - (pt.price - minP) / (maxP - minP));
            ctx.lineTo(x, y);
        });
        ctx.lineTo(w - padding, h - padding);
        ctx.closePath();
        ctx.fill();

        // Draw prediction point
        const lastPt = data.history[data.history.length - 1];
        const lastX = w - padding;
        const lastY = padding + (h - 2 * padding) * (1 - (lastPt.price - minP) / (maxP - minP));

        ctx.fillStyle = '#34d399';
        ctx.shadowColor = '#34d399';
        ctx.shadowBlur = 20;
        ctx.beginPath();
        ctx.arc(lastX, lastY, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;

        // Labels
        ctx.fillStyle = '#94a3b8';
        ctx.font = '12px Inter';
        ctx.fillText('60 Days', padding, h - 15);
        ctx.fillText('Today', w - padding - 30, h - 15);
        ctx.fillText(`$${maxP.toFixed(0)}`, 10, padding + 5);
        ctx.fillText(`$${minP.toFixed(0)}`, 10, h - padding - 5);

        // Title
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 14px Orbitron';
        ctx.fillText(`${data.ticker} Price History & Prediction`, padding, 25);
    }

    // ============================================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ============================================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ============================================================
    // PARALLAX EFFECT ON HERO
    // ============================================================
    const heroContent = document.querySelector('.hero-content');
    if (heroContent) {
        window.addEventListener('scroll', () => {
            const scrolled = window.scrollY;
            if (scrolled < window.innerHeight) {
                heroContent.style.transform = `translateY(${scrolled * 0.3}px)`;
                heroContent.style.opacity = 1 - (scrolled / window.innerHeight) * 0.8;
            }
        });
    }

    // ============================================================
    // GLITCH EFFECT ON HOVER (for specific elements)
    // ============================================================
    const glitchElements = document.querySelectorAll('.glitch-text');
    glitchElements.forEach(el => {
        const original = el.textContent;
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&';

        el.addEventListener('mouseenter', () => {
            let iterations = 0;
            const interval = setInterval(() => {
                el.textContent = original.split('').map((char, i) => {
                    if (i < iterations) return original[i];
                    return chars[Math.floor(Math.random() * chars.length)];
                }).join('');

                if (iterations >= original.length) clearInterval(interval);
                iterations += 1/3;
            }, 30);
        });
    });

});
