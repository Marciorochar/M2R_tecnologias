/* Progressive decoration: content and the static SVG never depend on this file. */
(() => {
    'use strict';
    const NS = 'http://www.w3.org/2000/svg';
    const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
    document.querySelectorAll('.page-hero--circuits').forEach(async (hero) => {
        if (hero.dataset.internalHeroReady) return;
        hero.dataset.internalHeroReady = 'true';
        const image = hero.querySelector('.internal-hero-art');
        const control = hero.querySelector('[data-internal-hero-motion]');
        if (!image || !control) return;
        let manualPause = false;
        let onScreen = hero.getBoundingClientRect().bottom > 0 && hero.getBoundingClientRect().top < innerHeight;
        let enhanced = false;
        const sync = () => {
            const paused = manualPause || preference.matches || document.hidden || !onScreen;
            hero.classList.toggle('internal-hero-paused', paused);
            control.hidden = !enhanced || preference.matches;
            control.setAttribute('aria-pressed', String(manualPause));
            control.textContent = manualPause ? 'Retomar movimento' : 'Pausar movimento';
            control.setAttribute('aria-label', `${control.textContent} do destaque`);
            if (preference.matches) hero.classList.remove('internal-hero-pointer');
        };
        control.addEventListener('click', () => { manualPause = !manualPause; sync(); });
        preference.addEventListener('change', sync);
        document.addEventListener('visibilitychange', sync);
        try {
            if ('IntersectionObserver' in window) {
                new IntersectionObserver(([entry]) => { onScreen = entry.isIntersecting; sync(); }).observe(hero);
            }
        } catch (_) { /* Scroll events below preserve lifecycle behavior. */ }
        window.addEventListener('scroll', () => {
            const bounds = hero.getBoundingClientRect();
            onScreen = bounds.bottom > 0 && bounds.top < innerHeight;
            sync();
        }, { passive: true });
        sync();
        try {
            const url = new URL(image.src, location.href);
            if (url.origin !== location.origin) return;
            const response = await fetch(url, { credentials: 'same-origin' });
            if (!response.ok) return;
            const documentSVG = new DOMParser().parseFromString(await response.text(), 'image/svg+xml');
            const source = [...documentSVG.querySelectorAll('path')];
            if (documentSVG.querySelector('parsererror') || source.length !== 14) return;
            // Construct only known geometry; never insert fetched markup into the page.
            const svg = document.createElementNS(NS, 'svg');
            svg.setAttribute('viewBox', '0 0 1200 610');
            svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');
            svg.setAttribute('aria-hidden', 'true');
            svg.setAttribute('focusable', 'false');
            svg.classList.add('internal-hero-live');
            source.forEach((original) => {
                const d = original.getAttribute('d');
                if (!d || !/^[MmLlHhVv\d\s.,+-]+$/.test(d)) throw new Error('Invalid circuit geometry');
                const path = document.createElementNS(NS, 'path');
                path.setAttribute('d', d);
                path.setAttribute('pathLength', '1');
                path.classList.add('internal-hero-pulse');
                svg.append(path);
            });
            const halo = document.createElementNS(NS, 'circle');
            halo.setAttribute('r', '110');
            halo.classList.add('internal-hero-halo');
            svg.append(halo);
            hero.prepend(svg);
            hero.addEventListener('pointermove', (event) => {
                if (preference.matches || manualPause || event.pointerType === 'touch') return;
                const point = svg.createSVGPoint();
                point.x = event.clientX;
                point.y = event.clientY;
                const matrix = svg.getScreenCTM();
                if (!matrix) return;
                const local = point.matrixTransform(matrix.inverse());
                halo.setAttribute('cx', local.x);
                halo.setAttribute('cy', local.y);
                hero.classList.add('internal-hero-pointer');
            }, { passive: true });
            hero.addEventListener('pointerleave', () => hero.classList.remove('internal-hero-pointer'));
            enhanced = true;
            sync();
        } catch (_) {
            // The decorative image and the gradient remain the usable fallback.
            sync();
        }
    });
})();
