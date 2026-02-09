document.addEventListener('DOMContentLoaded', () => {
    const aboutBtn = document.querySelector('.nav-link[href="#about"]');
    const folioBtn = document.querySelector('.nav-link[href="#folio"]');
    const overlays = document.querySelectorAll('.overlay');
    const closeBtns = document.querySelectorAll('.close-overlay');

    // Text Scramble Effect
    const scrambleText = (el, finalStr) => {
        const chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/";
        let iteration = 0;
        const interval = setInterval(() => {
            el.innerText = finalStr.split("").map((char, index) => {
                if (index < iteration) return finalStr[index];
                return chars[Math.floor(Math.random() * chars.length)];
            }).join("");
            if (iteration >= finalStr.length) clearInterval(interval);
            iteration += 1 / 3;
        }, 30);
    };

    // Modified Overlay Open with Scramble
    const openOverlay = (id) => {
        const target = document.querySelector(id);
        target.classList.add('active');
        const titles = target.querySelectorAll(".section-title");
        titles.forEach(title => scrambleText(title, title.innerText));

        gsap.fromTo(target.querySelectorAll(".content-box"),
            { y: 50, opacity: 0, rotationX: -10 },
            { y: 0, opacity: 1, rotationX: 0, duration: 0.8, stagger: 0.2, ease: "power2.out" }
        );
    };

    aboutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openOverlay('#about-overlay');
    });

    folioBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openOverlay('#folio-overlay');
    });

    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            btn.closest('.overlay').classList.remove('active');
        });
    });

    // Close on background click
    overlays.forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.classList.remove('active');
            }
        });
    });

    // Custom Cursor & Parallax Logic
    const cursor = document.querySelector('.cursor-follower');
    const bgContainer = document.querySelector('.background-container');

    document.addEventListener('mousemove', (e) => {
        // Spotlight follow
        gsap.to(cursor, {
            x: e.clientX,
            y: e.clientY,
            duration: 0.3,
            ease: "power2.out"
        });

        // Parallax depth
        const xPos = (e.clientX / window.innerWidth - 0.5) * 40;
        const yPos = (e.clientY / window.innerHeight - 0.5) * 40;
        gsap.to(bgContainer, {
            x: xPos,
            y: yPos,
            duration: 1,
            ease: "power1.out"
        });
    });

    // Hover effects for links
    const links = document.querySelectorAll('a, button');
    links.forEach(link => {
        link.addEventListener('mouseenter', () => {
            cursor.classList.add('hover');
        });
        link.addEventListener('mouseleave', () => {
            cursor.classList.remove('hover');
        });
    });

    // Audio Logic
    const music = document.getElementById('bg-music');
    const audioBtn = document.getElementById('audio-toggle');
    let isPlaying = false;

    const toggleAudio = () => {
        if (isPlaying) {
            music.pause();
            audioBtn.textContent = 'SOUND OFF';
        } else {
            music.play();
            audioBtn.textContent = 'SOUND ON';
        }
        isPlaying = !isPlaying;
    };

    audioBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent trigger from global mousedown
        toggleAudio();
    });

    // Modern browsers require interaction to play audio
    document.addEventListener('mousedown', () => {
        if (!isPlaying) {
            music.play().then(() => {
                isPlaying = true;
                audioBtn.textContent = 'SOUND ON';
            }).catch(error => {
                console.log("Autoplay prevented, waiting for user toggle.");
            });
        }
    }, { once: true });

    // Magnetic Navigation Logic
    const magneticLinks = document.querySelectorAll('.nav-link');
    magneticLinks.forEach(link => {
        link.addEventListener('mousemove', (e) => {
            const rect = link.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            gsap.to(link, {
                x: x * 0.4,
                y: y * 0.4,
                duration: 0.4,
                ease: "power2.out"
            });
        });
        link.addEventListener('mouseleave', () => {
            gsap.to(link, { x: 0, y: 0, duration: 0.6, ease: "elastic.out(1, 0.3)" });
        });
    });

    // 3D Card Tilt Logic
    const overlayContents = document.querySelectorAll('.overlay-content');
    document.addEventListener('mousemove', (e) => {
        overlayContents.forEach(content => {
            if (content.closest('.overlay').classList.contains('active')) {
                const rect = content.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width - 0.5;
                const y = (e.clientY - rect.top) / rect.height - 0.5;
                gsap.to(content, {
                    rotationY: x * 10,
                    rotationX: -y * 10,
                    duration: 0.6,
                    ease: "power2.out"
                });
            }
        });
    });

    // Dashboard Logic (WebSocket & Feed)
    const liveTrigger = document.querySelector('.live-trigger');
    const liveOverlay = document.getElementById('live-overlay');
    const btcPrice = document.querySelector('.symbol-card[data-symbol="BTCUSDT"] .price');
    const btcMeta = document.querySelector('.symbol-card[data-symbol="BTCUSDT"] .change');
    const ethPrice = document.querySelector('.symbol-card[data-symbol="ETHUSDT"] .price');
    const ethMeta = document.querySelector('.symbol-card[data-symbol="ETHUSDT"] .change');
    const liveLog = document.getElementById('live-log');
    const liveClock = document.getElementById('dashboard-clock');
    const canvas = document.getElementById('live-visualizer');
    const ctx = canvas.getContext('2d');

    let ws;
    let visualizerInterval;

    const drawVisualizer = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = '#00ff41';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(0, canvas.height / 2);
        for (let i = 0; i < canvas.width; i++) {
            const y = canvas.height / 2 + Math.sin(i * 0.05 + Date.now() * 0.01) * 20 * Math.random();
            ctx.lineTo(i, y);
        }
        ctx.stroke();
    };

    const connectWS = () => {
        if (ws) ws.close();
        // Correct Binance Combined Stream URL
        ws = new WebSocket('wss://stream.binance.com:9443/stream?streams=btcusdt@ticker/ethusdt@ticker');

        ws.onmessage = (event) => {
            const payload = JSON.parse(event.data);
            const data = payload.data;
            const symbol = data.s;
            const price = parseFloat(data.c).toFixed(2);
            const change = parseFloat(data.P).toFixed(2);
            const isUp = parseFloat(change) >= 0;

            const updateUI = (el, meta, val, pChange) => {
                const oldPrice = parseFloat(el.innerText);
                const newPrice = parseFloat(val);
                el.innerText = val;
                meta.innerText = `${pChange >= 0 ? '+' : ''}${pChange}%`;
                meta.className = `change ${pChange >= 0 ? 'up' : 'down'}`;

                if (newPrice > oldPrice) {
                    gsap.fromTo(el, { color: '#00ff41' }, { color: '#fff', duration: 0.5 });
                } else if (newPrice < oldPrice) {
                    gsap.fromTo(el, { color: '#ff3b3b' }, { color: '#fff', duration: 0.5 });
                }
            };

            if (symbol === 'BTCUSDT') {
                updateUI(btcPrice, btcMeta, price, change);
            } else if (symbol === 'ETHUSDT') {
                updateUI(ethPrice, ethMeta, price, change);
            }
        };

        ws.onopen = () => addLog('CORE_LINK: BINANCE_WS_ESTABLISHED');
        ws.onerror = (err) => addLog('CORE_ERR: WS_HANDSHAKE_FAILED');
        ws.onclose = () => {
            addLog('CORE_LINK: RECONNECTING...');
            setTimeout(connectWS, 5000);
        };
    };

    const addLog = (msg) => {
        const div = document.createElement('div');
        div.style.color = '#00ff41';
        div.style.opacity = '0.7';
        div.innerText = `[${new Date().toLocaleTimeString()}] > ${msg}`;
        liveLog.prepend(div);
        if (liveLog.children.length > 15) liveLog.lastChild.remove();
    };

    const updateClock = () => {
        const now = new Date();
        liveClock.innerText = now.toTimeString().split(' ')[0];
    };

    liveTrigger.addEventListener('click', (e) => {
        e.preventDefault();
        openOverlay('#live-overlay');
        connectWS();
        visualizerInterval = setInterval(drawVisualizer, 50);
        setInterval(updateClock, 1000);
        addLog('NEVERDIE_OS: SYSTEM_UP');
    });

    const closeDashboard = liveOverlay.querySelector('.close-overlay');
    closeDashboard.addEventListener('click', () => {
        if (ws) ws.close();
        clearInterval(visualizerInterval);
        addLog('NEVERDIE_OS: SESSION_HALT');
    });

    // Final Polish: Hero Scramble with longer text
    const heroH1 = document.querySelector('.hero-text h1');
    scrambleText(heroH1, "NEVERDIE\nQUANTUM REALM");
});

// Hero Text Interaction: Follow/Push effect
document.addEventListener('mousemove', (e) => {
    const rect = heroH1.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const dist = Math.sqrt(Math.pow(e.clientX - centerX, 2) + Math.pow(e.clientY - centerY, 2));

    if (dist < 300) {
        const range = (300 - dist) / 300;
        gsap.to(heroH1, {
            x: (e.clientX - centerX) * 0.15 * range,
            y: (e.clientY - centerY) * 0.15 * range,
            scale: 1 + (0.05 * range),
            duration: 0.4,
            ease: "power2.out"
        });
        cursor.classList.add('hover'); // Expand cursor when near text
    } else {
        gsap.to(heroH1, { x: 0, y: 0, scale: 1, duration: 0.8, ease: "elastic.out(1, 0.3)" });
        cursor.classList.remove('hover');
    }
});
