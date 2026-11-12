/* Interactive, brand-aligned golden circuits for the homepage hero only. */
(() => {
    'use strict';

    const hero = document.getElementById('m2r-hero');
    const svg = document.getElementById('m2r-circuits');
    if (!hero || !svg) return;

    const video = hero.querySelector('.home-hero-motion-video');
    const motionToggle = document.getElementById('m2r-motion-toggle');
    const sourcePaths = [...svg.querySelectorAll('#m2r-circuit-paths path')];
    const traces = document.getElementById('m2r-trace-render');
    const nodes = document.getElementById('m2r-node-render');
    const pulses = document.getElementById('m2r-pulse-render');
    const ripples = document.getElementById('m2r-ripple-render');
    const halo = document.getElementById('m2r-cursor-halo');
    const activate = document.getElementById('m2r-circuit-activate');
    const tip = document.getElementById('m2r-circuit-tip');
    if (!sourcePaths.length || !traces || !nodes || !pulses || !ripples || !halo || !activate || !tip) return;

    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const touch = window.matchMedia('(hover: none)');
    const svgNS = 'http://www.w3.org/2000/svg';
    const paths = [];
    const liveRipples = [];
    let pointer = null;
    let activeUntil = 0;
    let elapsed = 0;
    let frameHandle = null;
    let previousFrame = performance.now();
    let inView = true;
    let userPaused = false;
    let pendingPointer = null;

    function listenForMediaChange(query, callback) {
        if (typeof query.addEventListener === 'function') query.addEventListener('change', callback);
        else if (typeof query.addListener === 'function') query.addListener(callback);
    }

    function draw(name, attributes, parent) {
        const element = document.createElementNS(svgNS, name);
        Object.entries(attributes).forEach(([attribute, value]) => element.setAttribute(attribute, String(value)));
        parent.appendChild(element);
        return element;
    }

    function svgPoint(event) {
        const point = svg.createSVGPoint();
        point.x = event.clientX;
        point.y = event.clientY;
        const matrix = svg.getScreenCTM();
        return matrix ? point.matrixTransform(matrix.inverse()) : { x: 900, y: 305 };
    }

    function defaultTip() {
        return touch.matches ? 'Toque para enviar um pulso' : 'Ativar circuitos';
    }

    // Keep source geometry in the markup for a deterministic, testable design.
    sourcePaths.forEach((source, index) => {
        const d = source.getAttribute('d');
        draw('path', { d, class: 'm2r-trace-under' }, traces);
        const core = draw('path', { d, class: 'm2r-trace-core', stroke: 'url(#m2r-line-gold)' }, traces);
        const near = draw('path', { d, class: 'm2r-trace-near' }, traces);
        const length = source.getTotalLength();
        const samples = Array.from({ length: 37 }, (_, sample) => {
            const point = source.getPointAtLength(length * sample / 36);
            return { x: point.x, y: point.y };
        });
        const pulse = draw('circle', { class: 'm2r-light-pulse', cx: -100, cy: -100, r: index % 3 === 0 ? 3.5 : 2.6, opacity: 0.7 }, pulses);
        for (const fraction of [0.23, 0.56, 0.79, 1]) {
            const point = source.getPointAtLength(length * fraction);
            draw('circle', { class: 'm2r-circuit-node', cx: point.x, cy: point.y, r: fraction === 1 ? 3.1 : 2 }, nodes);
        }
        paths.push({ source, core, near, length, samples, pulse, phase: (index * 0.157) % 1, speed: 0.071 + index * 0.007, proximity: 0 });
    });

    const cursorNode = draw('circle', { class: 'm2r-node-active', r: 4.8, cx: -100, cy: -100, opacity: 0 }, nodes);

    function nearestOnPath(path, point) {
        let bestDistance = Infinity;
        let bestPoint = null;
        for (const candidate of path.samples) {
            const distance = Math.hypot(candidate.x - point.x, candidate.y - point.y);
            if (distance < bestDistance) {
                bestDistance = distance;
                bestPoint = candidate;
            }
        }
        return { distance: bestDistance, point: bestPoint };
    }

    function onPointerMove(event) {
        if (touch.matches || reducedMotion.matches || userPaused) return;
        pendingPointer = { clientX: event.clientX, clientY: event.clientY };
    }

    function updatePointer(event) {
        pointer = svgPoint(event);
        const rect = hero.getBoundingClientRect();
        const x = 100 * (event.clientX - rect.left) / rect.width;
        const y = 100 * (event.clientY - rect.top) / rect.height;
        hero.style.setProperty('--cursor-x', `${x}%`);
        hero.style.setProperty('--cursor-y', `${y}%`);
        hero.style.setProperty('--cursor-glow', '.075');
        hero.style.setProperty('--parallax-x', `${((x - 50) * -0.085).toFixed(1)}px`);
        hero.style.setProperty('--parallax-y', `${((y - 50) * -0.05).toFixed(1)}px`);
        halo.setAttribute('cx', pointer.x);
        halo.setAttribute('cy', pointer.y);
        let closest = { distance: Infinity, point: null };
        for (const path of paths) {
            const hit = nearestOnPath(path, pointer);
            path.proximity = Math.max(0, 1 - hit.distance / 130);
            if (hit.distance < closest.distance) {
                closest = { distance: hit.distance, point: hit.point };
            }
        }
        if (closest.point && closest.distance < 112) {
            cursorNode.setAttribute('cx', closest.point.x);
            cursorNode.setAttribute('cy', closest.point.y);
            cursorNode.setAttribute('opacity', String(0.85 * (1 - closest.distance / 112)));
        } else {
            cursorNode.setAttribute('opacity', '0');
        }
        halo.classList.toggle('active', closest.distance < 130);
        if (!activeUntil) tip.textContent = closest.distance < 130
            ? 'Clique para enviar um pulso de energia'
            : defaultTip();
    }

    function onPointerLeave() {
        pendingPointer = null;
        pointer = null;
        paths.forEach(path => { path.proximity = 0; });
        cursorNode.setAttribute('opacity', '0');
        hero.style.setProperty('--cursor-glow', '.02');
        hero.style.setProperty('--parallax-x', '0px');
        hero.style.setProperty('--parallax-y', '0px');
        halo.classList.remove('active');
        if (!activeUntil) tip.textContent = defaultTip();
    }

    function energize(position) {
        if (reducedMotion.matches || userPaused) return;
        const now = performance.now();
        activeUntil = now + 1750;
        tip.textContent = 'Pulso enviado';
        const ring = draw('circle', { cx: position.x, cy: position.y, r: 3, fill: 'none', stroke: '#ffe3a5', 'stroke-width': 2, opacity: 0.82 }, ripples);
        liveRipples.push({ ring, born: now });
        paths.forEach((path, index) => { path.phase = (index * 0.057 + 0.02) % 1; });
    }

    function frame(now) {
        frameHandle = null;
        if (reducedMotion.matches || document.hidden || !inView) return;
        const frameInterval = 1000 / 30;
        if (touch.matches && now - previousFrame < frameInterval - 2) {
            frameHandle = window.requestAnimationFrame(frame);
            return;
        }
        const delta = Math.min(0.04, (now - previousFrame) / 1000);
        previousFrame = now;
        if (pendingPointer) {
            const latestPointer = pendingPointer;
            pendingPointer = null;
            updatePointer(latestPointer);
        }
        elapsed += delta;
        const boosted = now < activeUntil;
        if (!boosted && activeUntil !== 0) {
            activeUntil = 0;
            tip.textContent = defaultTip();
        }

        paths.forEach((path, index) => {
            path.phase = (path.phase + delta * path.speed * (boosted ? 5.8 : 1)) % 1;
            const position = path.source.getPointAtLength(path.length * path.phase);
            path.pulse.setAttribute('cx', position.x);
            path.pulse.setAttribute('cy', position.y);
            path.pulse.setAttribute('opacity', boosted ? '.95' : String(0.38 + 0.24 * Math.sin(elapsed * 1.8 + index)));
            path.pulse.setAttribute('r', boosted ? '4.2' : '2.7');
            const light = Math.max(path.proximity, boosted ? 0.45 : 0);
            path.near.style.opacity = String((light * 0.72).toFixed(2));
            path.core.style.opacity = String(Math.min(1, 0.45 + path.proximity * 0.65 + (boosted ? 0.3 : 0)));
        });

        for (let i = liveRipples.length - 1; i >= 0; i--) {
            const ripple = liveRipples[i];
            const progress = (now - ripple.born) / 1000;
            if (progress > 1.1) {
                ripple.ring.remove();
                liveRipples.splice(i, 1);
                continue;
            }
            ripple.ring.setAttribute('r', 5 + progress * 95);
            ripple.ring.setAttribute('opacity', String(Math.max(0, 0.8 * (1 - progress / 1.1))));
        }
        frameHandle = window.requestAnimationFrame(frame);
    }

    function refreshAnimation() {
        const shouldAnimate = !reducedMotion.matches && !document.hidden && inView && !userPaused;
        if (video) {
            if (shouldAnimate) video.play().catch(() => {});
            else video.pause();
        }
        if (!shouldAnimate && frameHandle !== null) {
            window.cancelAnimationFrame(frameHandle);
            frameHandle = null;
        }
        if (shouldAnimate && frameHandle === null) {
            previousFrame = performance.now() - (touch.matches ? 1000 / 30 : 1000 / 60);
            frameHandle = window.requestAnimationFrame(frame);
        }
        if (motionToggle) motionToggle.hidden = reducedMotion.matches;
        if (reducedMotion.matches) {
            onPointerLeave();
            tip.textContent = 'Movimento reduzido ativo';
            activate.disabled = true;
        } else if (userPaused) {
            onPointerLeave();
            tip.textContent = 'Animação pausada';
            activate.disabled = true;
        } else {
            activate.disabled = false;
            if (!activeUntil) {
                tip.textContent = defaultTip();
            }
        }
    }

    hero.addEventListener('pointermove', onPointerMove, { passive: true });
    hero.addEventListener('pointerleave', onPointerLeave);
    hero.addEventListener('click', event => {
        if (event.target.closest('a, button, .home-hero-copy')) return;
        const position = svgPoint(event);
        if (paths.some(path => nearestOnPath(path, position).distance < 85)) energize(position);
    });
    activate.addEventListener('click', () => energize({ x: 955, y: 318 }));
    if (motionToggle) {
        motionToggle.setAttribute('aria-pressed', 'false');
        motionToggle.hidden = reducedMotion.matches;
        motionToggle.addEventListener('click', () => {
            userPaused = !userPaused;
            motionToggle.setAttribute('aria-pressed', String(userPaused));
            motionToggle.title = userPaused ? 'Retomar movimento' : 'Pausar movimento';
            refreshAnimation();
        });
    }
    listenForMediaChange(reducedMotion, refreshAnimation);
    document.addEventListener('visibilitychange', refreshAnimation);
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(entries => {
            inView = entries[0].isIntersecting;
            refreshAnimation();
        }, { threshold: 0 });
        observer.observe(hero);
    }
    refreshAnimation();
})();
