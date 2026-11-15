/* Progressive enhancement shared by the Home and every internal hero. */
(() => {
    'use strict';

    const NS = 'http://www.w3.org/2000/svg';
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const listen = (target, type, callback) => {
        if (typeof target.addEventListener === 'function') target.addEventListener(type, callback);
        else if (typeof target.addListener === 'function') target.addListener(callback);
    };

    function enhance(root) {
        if (root.dataset.heroSystemReady) return;
        root.dataset.heroSystemReady = 'true';

        const image = root.querySelector('.hero-system__art');
        const control = root.querySelector('[data-hero-motion]');
        if (!image) return;

        let manualPause = false;
        let enhanced = false;
        let liveSvg = null;
        let liveHalo = null;
        let inView = (() => {
            const bounds = root.getBoundingClientRect();
            return bounds.bottom > 0 && bounds.top < window.innerHeight;
        })();

        function sync() {
            const paused = manualPause || reducedMotion.matches || document.hidden || !inView;
            root.classList.toggle('hero-system--paused', paused);
            if (paused) root.classList.remove('hero-system--pointer');
            if (!control) return;
            control.hidden = !enhanced || reducedMotion.matches;
            control.setAttribute('aria-pressed', String(manualPause));
            control.textContent = manualPause ? 'Retomar movimento' : 'Pausar movimento';
            control.setAttribute('aria-label', `${control.textContent} do destaque`);
        }

        if (control) {
            control.addEventListener('click', () => {
                manualPause = !manualPause;
                sync();
            });
        }
        root.addEventListener('pointermove', event => {
            if (!enhanced || reducedMotion.matches || root.classList.contains('hero-system--paused') || event.pointerType === 'touch') return;
            const point = liveSvg.createSVGPoint();
            point.x = event.clientX;
            point.y = event.clientY;
            const matrix = liveSvg.getScreenCTM();
            if (!matrix) return;
            const local = point.matrixTransform(matrix.inverse());
            liveHalo.setAttribute('cx', local.x);
            liveHalo.setAttribute('cy', local.y);
            root.classList.add('hero-system--pointer');
        }, { passive: true });
        root.addEventListener('pointerleave', () => root.classList.remove('hero-system--pointer'));
        listen(reducedMotion, 'change', sync);
        document.addEventListener('visibilitychange', sync);

        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver(([entry]) => {
                inView = entry.isIntersecting;
                sync();
            }, { threshold: 0 });
            observer.observe(root);
        } else {
            const refreshVisibility = () => {
                const bounds = root.getBoundingClientRect();
                inView = bounds.bottom > 0 && bounds.top < window.innerHeight;
                sync();
            };
            window.addEventListener('scroll', refreshVisibility, { passive: true });
            window.addEventListener('resize', refreshVisibility, { passive: true });
        }

        sync();
        const url = new URL(image.getAttribute('src'), window.location.href);
        if (url.origin !== window.location.origin) return;

        fetch(url.href, { credentials: 'same-origin' })
            .then(response => {
                if (!response.ok) throw new Error('Circuit artwork unavailable');
                return response.text();
            })
            .then(markup => {
                const parsed = new DOMParser().parseFromString(markup, 'image/svg+xml');
                const sourcePaths = [...parsed.querySelectorAll('svg path')];
                if (parsed.querySelector('parsererror') || sourcePaths.length !== 14) throw new Error('Circuit artwork invalid');

                const svg = document.createElementNS(NS, 'svg');
                svg.setAttribute('viewBox', '0 0 1200 610');
                svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');
                svg.setAttribute('aria-hidden', 'true');
                svg.setAttribute('focusable', 'false');
                svg.classList.add('hero-system__live');

                sourcePaths.forEach(source => {
                    const d = source.getAttribute('d');
                    if (!d || !/^[MmLlHhVv\d\s.,+-]+$/.test(d)) throw new Error('Circuit geometry invalid');
                    const path = document.createElementNS(NS, 'path');
                    path.setAttribute('d', d);
                    path.setAttribute('pathLength', '1');
                    path.classList.add('hero-system__pulse');
                    svg.append(path);
                });

                const halo = document.createElementNS(NS, 'circle');
                halo.setAttribute('r', '110');
                halo.classList.add('hero-system__halo');
                svg.append(halo);
                liveSvg = svg;
                liveHalo = halo;
                image.insertAdjacentElement('afterend', svg);
                const paths = [...svg.querySelectorAll('.hero-system__pulse')];
                enhanced = true;
                sync();
                root.dispatchEvent(new CustomEvent('m2rhero:ready', { detail: { svg, paths } }));
            })
            .catch(() => {
                // The static image and readable page content remain available.
                sync();
            });
    }

    document.querySelectorAll('[data-hero-system]').forEach(enhance);
})();
