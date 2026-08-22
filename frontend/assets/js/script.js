document.addEventListener('DOMContentLoaded', initApp);

function initApp() {
    /*
        =====================================================
        M2R TECNOLOGIAS - SCRIPT PRINCIPAL
        Funções:
        1. Rolagem suave para links internos
        2. Atualização automática do item ativo no menu
        3. Animação fade-in ao rolar a página
        4. Envio do formulário de contato
        =====================================================
    */

    // --- FUNÇÕES UTILITÁRIAS GLOBAIS ---
    const setFormStatus = (element, message, type) => {
        if (!element) return;
        element.textContent = message;
        if (type === 'success') element.style.color = '#166534';
        else if (type === 'error') element.style.color = '#b91c1c';
        else if (type === 'sending') element.style.color = 'var(--color-text-secondary)';
    };

    // Define o link ativo no menu dinamicamente com base na URL
    const normalizePage = (path) => {
        const page = (path || '').split('/').pop() || 'index';
        return page.replace('.html', '') || 'index';
    };
    const currentPath = normalizePage(window.location.pathname);
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.classList.remove('active');
        const linkPath = normalizePage(link.getAttribute('href'));
        if (linkPath === currentPath) {
            link.classList.add('active');
        }
    });

    // Seleciona apenas os links do menu, sem pegar o link da logo
    const navbarLinks = document.querySelectorAll('.nav-links a');

    // Seleciona todas as seções que possuem ID
    const sections = document.querySelectorAll('section[id]');

    // Seleciona a navbar para calcular o deslocamento na rolagem
    const navbar = document.querySelector('.navbar');

    /*
        =====================================================
        0. NAVBAR INTERATIVA E MENU MOBILE (HAMBÚRGUER)
        =====================================================
    */
    if (navbar) {
        // Efeito de scroll (Shrink/Shadow)
        window.addEventListener('scroll', () => {
            if (window.scrollY > 20) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        // Criação dinâmica do botão Hambúrguer para mobile
        const mobileBtn = document.createElement('button');
        mobileBtn.className = 'mobile-menu-btn';
        mobileBtn.innerHTML = '☰';
        mobileBtn.setAttribute('aria-label', 'Abrir menu mobile');
        mobileBtn.setAttribute('aria-expanded', 'false');
        
        const navLinks = navbar.querySelector('.nav-links');
        if (navLinks) {
            navbar.insertBefore(mobileBtn, navLinks);
        }

        // Lógica de abrir/fechar o menu mobile
        mobileBtn.addEventListener('click', () => {
            const isOpen = navbar.classList.toggle('menu-open');
            mobileBtn.innerHTML = isOpen ? '✕' : '☰';
            mobileBtn.setAttribute('aria-expanded', isOpen.toString());
        });

        // Fechar o menu ao clicar em um link
        const links = navbar.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    navbar.classList.remove('menu-open');
                    mobileBtn.innerHTML = '☰';
                }
            });
        });
    }

    /*
        =====================================================
        1. ATUALIZAÇÃO DO LINK ATIVO NO MENU
        =====================================================
    */

    const updateActiveLink = (sectionId) => {
        const matchingLink = document.querySelector(`.nav-links a[href="#${sectionId}"]`);

        // Só atualiza o menu se existir um link interno correspondente
        // Isso evita remover o "active" da página projetos.html
        if (!matchingLink) return;

        navbarLinks.forEach(link => {
            link.classList.remove('active');
        });

        matchingLink.classList.add('active');
    };

    /*
        =====================================================
        2. ROLAGEM SUAVE PARA LINKS INTERNOS
        =====================================================
    */

    navbarLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            const href = this.getAttribute('href');

            // Ignora links vazios
            if (!href) return;

            // Aplica rolagem suave apenas para links internos da mesma página
            if (href.startsWith('#')) {
                event.preventDefault();

                const targetId = href.substring(1);
                const targetSection = document.getElementById(targetId);

                if (targetSection) {
                    const navbarHeight = navbar ? navbar.offsetHeight : 0;
                    const targetPosition = targetSection.offsetTop - navbarHeight;

                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });

                    navbarLinks.forEach(navLink => {
                        navLink.classList.remove('active');
                    });

                    this.classList.add('active');
                }
            }

            // Links para outras páginas e âncoras internas funcionam normalmente
        });
    });

    /*
        =====================================================
        3. OBSERVER PARA LINK ATIVO DO MENU
        =====================================================
    */

    const linkedSections = Array.from(sections).filter(section => {
        return document.querySelector(`.nav-links a[href="#${section.id}"]`);
    });

    if ('IntersectionObserver' in window && linkedSections.length > 0) {
        const activeLinkObserverOptions = {
            root: null,
            rootMargin: '-30% 0px -55% 0px',
            threshold: 0
        };

        const activeLinkObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateActiveLink(entry.target.id);
                }
            });
        }, activeLinkObserverOptions);

        linkedSections.forEach(section => {
            activeLinkObserver.observe(section);
        });
    }

    /*
        =====================================================
        4. ANIMAÇÃO FADE-IN NAS SEÇÕES
        =====================================================
    */

    const fadeInSections = document.querySelectorAll('.fade-in-section');

    if ('IntersectionObserver' in window && fadeInSections.length > 0) {
        const fadeInObserverOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.15
        };

        const fadeInObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');

                    // Para de observar após a animação
                    observer.unobserve(entry.target);
                }
            });
        }, fadeInObserverOptions);

        fadeInSections.forEach(section => {
            fadeInObserver.observe(section);
        });
    } else {
        // Caso o navegador não suporte IntersectionObserver
        fadeInSections.forEach(section => {
            section.classList.add('is-visible');
        });
    }

    /*
        =====================================================
        5. FORMULARIO DE CONTATO
        =====================================================
    */

    const contactForm = document.getElementById('contact-form');
    const formStatus = document.getElementById('form-status');
    const contactRecipient = 'marciinhofla@gmail.com';

    if (contactForm && formStatus) {
        contactForm.addEventListener('submit', function (event) {
            event.preventDefault();

            if (!contactForm.checkValidity()) {
                contactForm.reportValidity();
                setFormStatus(formStatus, 'Preencha os campos obrigatórios corretamente.', 'error');
                return;
            }

            const name = (document.getElementById('name')?.value || '').trim();
            const email = (document.getElementById('email')?.value || '').trim();
            const phone = (document.getElementById('phone')?.value || '').trim();
            const message = (document.getElementById('message')?.value || '').trim();

            if (!name || !email || !message) {
                setFormStatus(formStatus, 'Preencha nome, e-mail e mensagem.', 'error');
                return;
            }

            const subject = encodeURIComponent(`Contato pelo site M2R - ${name}`);
            const body = encodeURIComponent(
                `Nome: ${name}\n` +
                `E-mail: ${email}\n` +
                `Telefone: ${phone || 'Não informado'}\n\n` +
                `Mensagem:\n${message}`
            );

            window.location.href = `mailto:${contactRecipient}?subject=${subject}&body=${body}`;
            setFormStatus(formStatus, 'Seu aplicativo de e-mail foi aberto para concluir o envio.', 'success');
        });
    }

}
