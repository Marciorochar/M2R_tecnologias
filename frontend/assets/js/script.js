// Configuração global da API (Detecta automaticamente Local vs Produção)
const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_URL = isLocalhost ? "http://127.0.0.1:5000" : "https://m2r-backend.onrender.com";

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
        5. Modais de telefone e e-mail
        6. Botão copiar contato
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
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.classList.remove('active');
        const linkPath = (link.getAttribute('href') || '').split('/').pop();
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

    if (contactForm && formStatus) {
        contactForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const name = document.getElementById('name')?.value || '';
            const email = document.getElementById('email')?.value || '';
            const phone = document.getElementById('phone')?.value || '';
            const message = document.getElementById('message')?.value || '';

            const formButton = this.querySelector('button[type="submit"]') || this.querySelector('button');

            if (formButton) {
                formButton.disabled = true;
                formButton.textContent = 'Enviando...';
            }

            setFormStatus(formStatus, 'Enviando sua mensagem...', 'sending');

            fetch(`${API_URL}/api/contato`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, phone, message })
            })
                .then(async response => {
                    let data;
                    try { data = await response.json(); } catch(e) {}
                    if (response.ok) {
                        setFormStatus(formStatus, data?.message || 'Mensagem enviada com sucesso.', 'success');
                        contactForm.reset();
                    } else {
                        setFormStatus(formStatus, data?.error || 'Não foi possível enviar a mensagem.', 'error');
                    }
                })
                .catch(() => {
                    setFormStatus(formStatus, 'Erro de conexão. Verifique sua internet e tente novamente.', 'error');
                })
                .finally(() => {
                    if (formButton) {
                        formButton.disabled = false;
                        formButton.textContent = 'Enviar mensagem';
                    }
                });
        });
    }

    /*
        =====================================================
        6. FUNÇÃO AUXILIAR PARA COPIAR TEXTO
        =====================================================
    */

    const copyTextToClipboard = async (text) => {
        const cleanText = text.trim();

        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(cleanText);
            return;
        }

        // Alternativa para navegadores ou ambientes sem HTTPS
        const textarea = document.createElement('textarea');
        textarea.value = cleanText;
        textarea.style.position = 'fixed';
        textarea.style.left = '-9999px';

        document.body.appendChild(textarea);
        textarea.focus();
        textarea.select();

        document.execCommand('copy');
        document.body.removeChild(textarea);
    };

    /*
        =====================================================
        7. MODAIS DE CONTATO
        =====================================================
    */

    const setupModal = (triggerBtnId, modalId) => {
        const triggerBtn = document.getElementById(triggerBtnId);
        const modal = document.getElementById(modalId);

        if (!triggerBtn || !modal) return;

        const closeModalBtn = modal.querySelector('.modal-close-btn');
        const copyBtns = modal.querySelectorAll('.copy-btn');

        const openModal = () => {
            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        };

        const closeModal = () => {
            modal.classList.add('hidden');
            document.body.style.overflow = '';
        };

        triggerBtn.addEventListener('click', (event) => {
            event.preventDefault();
            openModal();
        });

        if (closeModalBtn) {
            closeModalBtn.addEventListener('click', closeModal);
        }

        modal.addEventListener('click', (event) => {
            if (event.target === modal) {
                closeModal();
            }
        });

        copyBtns.forEach(button => {
            button.addEventListener('click', async () => {
                const textElement = button.previousElementSibling;

                if (!textElement) return;

                try {
                    await copyTextToClipboard(textElement.textContent);

                    button.textContent = 'Copiado!';

                    setTimeout(() => {
                        button.textContent = 'Copiar';
                    }, 2000);
                } catch (error) {
                    button.textContent = 'Erro';

                    setTimeout(() => {
                        button.textContent = 'Copiar';
                    }, 2000);
                }
            });
        });
    };

    setupModal('phone-contact-btn', 'phone-modal');
    setupModal('email-contact-btn', 'email-modal');

    /*
        =====================================================
        8. FECHAR MODAIS COM A TECLA ESC
        =====================================================
    */

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal-overlay:not(.hidden)');

            openModals.forEach(modal => {
                modal.classList.add('hidden');
            });

            document.body.style.overflow = '';
        }
    });

}
