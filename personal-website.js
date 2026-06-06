// Configuração global da API apontando diretamente para produção (Render)
const API_URL = "https://m2r-backend.onrender.com";

document.addEventListener('DOMContentLoaded', async () => {
    // --- VERIFICAÇÃO DE SEGURANÇA (ÁREA RESTRITA) ---
    const userToken = localStorage.getItem('m2r_token');
    const isAuthPage = document.body.classList.contains('page-auth');
    
    // Helper para redirecionar para a página de login correta dependendo da pasta
    const redirectToLogin = () => {
        const path = window.location.pathname.toLowerCase();
        if (path.includes('/login/site/')) {
            window.location.href = '../../login.html';
        } else if (path.includes('/login/')) {
            window.location.href = '../login.html';
        } else {
            window.location.href = 'login.html';
        }
    };
    
    // 1. Verificação Client-Side Rápida
    if (!userToken && !isAuthPage) {
        redirectToLogin();
        return;
    }

    // 2. Verificação Ativa com o Backend (Validar o JWT)
    if (userToken && !isAuthPage) {
        try {
            const response = await fetch(`${API_URL}/verify`, {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${userToken}` }
            });
            if (!response.ok) {
                localStorage.removeItem('m2r_token');
                localStorage.removeItem('m2r_userName');
                document.cookie = 'm2r_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
                redirectToLogin();
                return;
            }
        } catch (error) {
            console.error('Erro de conexão ao verificar segurança do backend:', error);
        }
    }

    // 1. CARREGAR COMPONENTES (NAVBAR E FOOTER)
    await loadComponents();

    // 2. INICIALIZAR LÓGICA DO SITE
    initApp();
});

async function loadComponents() {
    try {
        // Descobre se estamos numa subpasta para acertar o caminho do rodapé/navbar
        const path = window.location.pathname.toLowerCase();
        let prefix = '';
        if (path.includes('/login/site/')) {
            prefix = '../../';
        } else if (path.includes('/login/')) {
            prefix = '../';
        }

        const navbarPlaceholder = document.getElementById('navbar-placeholder');
        if (navbarPlaceholder) {
            const navbarRes = await fetch(prefix + 'navbar.html');
            if (navbarRes.ok) navbarPlaceholder.innerHTML = await navbarRes.text();
        }

        const footerPlaceholder = document.getElementById('footer-placeholder');
        if (footerPlaceholder) {
            const footerRes = await fetch(prefix + 'footer.html');
            if (footerRes.ok) footerPlaceholder.innerHTML = await footerRes.text();
        }
    } catch (error) {
        console.error('Erro ao carregar componentes:', error);
    }
}

function initApp() {
    /*
        =====================================================
        M2R TECNOLOGIAS - SCRIPT PRINCIPAL
        Funções:
        1. Rolagem suave para links internos
        2. Atualização automática do item ativo no menu
        3. Animação fade-in ao rolar a página
        4. Envio do formulário de contato via Formspree
        5. Modais de telefone e e-mail
        6. Botão copiar contato
        7. Integração de Login e Cadastro com o Backend
        8. Animação interativa na tela de Login
        9. Sistema de Logout
        =====================================================
    */

    // --- FUNÇÕES UTILITÁRIAS GLOBAIS ---
    const setFormStatus = (element, message, type) => {
        if (!element) return;
        element.textContent = message;
        if (type === 'success') element.style.color = '#a7f3d0';
        else if (type === 'error') element.style.color = '#fca5a5';
        else if (type === 'sending') element.style.color = '#f5f5f5';
    };

    const redirectBasedOnPath = (targetPage) => {
        const path = window.location.pathname.toLowerCase();
        if (path.includes('/login/site/')) {
            window.location.href = targetPage === 'login.html' ? '../../login.html' : targetPage;
        } else if (path.includes('/login/')) {
            window.location.href = targetPage === 'login.html' ? '../login.html' : `Site/${targetPage}`;
        } else {
            window.location.href = targetPage === 'login.html' ? 'login.html' : `Login/Site/${targetPage}`;
        }
    };

    // --- 9. SISTEMA DE LOGOUT (Botão Sair) ---
    const userToken = localStorage.getItem('m2r_token');
    if (userToken && !document.body.classList.contains('page-auth')) {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            // Cria um grupo separado apenas para o perfil e botão de sair
            const userProfileContainer = document.createElement('div');
            userProfileContainer.className = 'user-profile-container';

            const logoutBtn = document.createElement('a');
            logoutBtn.href = '#';
            logoutBtn.textContent = 'Sair da Conta';
            logoutBtn.style.color = '#cc0000'; // Vermelho para destacar
            logoutBtn.style.fontWeight = 'bold';
            logoutBtn.style.textDecoration = 'none';
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                localStorage.removeItem('m2r_token'); // Destrói a chave de acesso
                localStorage.removeItem('m2r_userName'); // Destrói o nome salvo
                document.cookie = 'm2r_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT'; // Remove o cookie
                redirectBasedOnPath('login.html');
            });
            
            // Tenta resgatar o nome do usuário salvo
            const userName = localStorage.getItem('m2r_userName');
            if (userName) {
                const firstName = userName.split(' ')[0]; // Pega só o primeiro nome
                const greeting = document.createElement('span');
                greeting.textContent = `Olá, ${firstName}`;
                greeting.style.fontWeight = 'bold';
                greeting.style.color = 'var(--color-primary)';
                userProfileContainer.appendChild(greeting);
                
                // Atualiza o título grande da página inicial se ele existir
                const welcomeTitle = document.getElementById('welcome-title');
                if (welcomeTitle) welcomeTitle.textContent = `Bem-vindo(a), ${firstName}!`;
            }

            userProfileContainer.appendChild(logoutBtn);
            navbar.appendChild(userProfileContainer);
        }
    }

    // Define o link ativo no menu dinamicamente com base na URL
    const currentPath = window.location.pathname.split('/').pop() || 'index_inicio.html';
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
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
        1. ATUALIZAÇÃO DO LINK ATIVO NO MENU
        =====================================================
    */

    const updateActiveLink = (sectionId) => {
        const matchingLink = document.querySelector(`.nav-links a[href="#${sectionId}"]`);

        // Só atualiza o menu se existir um link interno correspondente
        // Isso evita remover o "active" da página index_projetos.html
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

            // Links como index.html#contact e index_projetos.html funcionam normalmente
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
        5. FORMULÁRIO DE CONTATO - FORMSPREE
        =====================================================
    */

    const contactForm = document.getElementById('contact-form');
    const formStatus = document.getElementById('form-status');

    if (contactForm && formStatus) {
        contactForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const name = document.getElementById('name')?.value || '';
            const email = document.getElementById('email')?.value || '';
            const message = document.getElementById('message')?.value || '';

            const formButton = this.querySelector('button[type="submit"]') || this.querySelector('button');

            if (formButton) {
                formButton.disabled = true;
                formButton.textContent = 'Enviando...';
            }

            setFormStatus(formStatus, 'Enviando sua mensagem...', 'sending');

            fetch(`${API_URL}/send-email`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, message })
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

    /*
        =====================================================
        9. SISTEMA DE LOGIN E CADASTRO (INTEGRAÇÃO BACKEND)
        =====================================================
    */

    // --- Lógica do Formulário de Cadastro ---
    const registerForm = document.getElementById('register-form');
    const registerStatus = document.getElementById('register-status');

    if (registerForm) {
        registerForm.addEventListener('submit', async function (event) {
            event.preventDefault(); // Bloqueia o redirecionamento automático do HTML

            const name = document.getElementById('register-name')?.value;
            const email = document.getElementById('register-email')?.value;
            const password = document.getElementById('register-password')?.value;
            const usuario = document.getElementById('register-usuario')?.value;
            const idade = document.getElementById('register-idade')?.value;
            const submitBtn = this.querySelector('button[type="submit"]');

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Verificando e Cadastrando...';
            }

            try {
                const response = await fetch(`${API_URL}/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, password, usuario, idade })
                });

                let data;
                try {
                    data = await response.json();
                } catch (parseError) {
                    console.error("Erro ao ler resposta do Python:", parseError);
                    throw new Error("O Python apresentou um erro interno. Verifique o terminal do VS Code.");
                }

                if (response.ok) {
                    if (registerStatus) setFormStatus(registerStatus, data.message, 'success');
                    
                    // Cadastro bem-sucedido: Salva o token de sessão (auto-login)
                    if (data.token) {
                        localStorage.setItem('m2r_token', data.token);
                        localStorage.setItem('m2r_userName', data.nome || name); // Salva o nome
                        document.cookie = `m2r_token=${data.token}; path=/; max-age=86400; Secure; SameSite=Lax`; // Salva no cookie
                    }

                    // Redireciona diretamente para a página de início
                    setTimeout(() => {
                        redirectBasedOnPath('index_inicio.html');
                    }, 1500);
                } else {
                    if (registerStatus) setFormStatus(registerStatus, data.error || 'Erro ao realizar cadastro.', 'error');
                }
            } catch (error) {
                console.error("Erro no fetch:", error);
                if (registerStatus) setFormStatus(registerStatus, error.message.includes('Python') ? error.message : `Falha de Conexão: ${error.message}. O Python está rodando?`, 'error');
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Cadastrar';
                }
            }
        });
    }

    // --- Lógica do Formulário de Login ---
    const loginForm = document.getElementById('login-form');
    const loginStatus = document.getElementById('login-status');

    // Ao carregar a página de login, verifica se há um e-mail salvo
    const savedEmail = localStorage.getItem('m2r_saved_email');
    const loginEmailInput = document.getElementById('login-email');
    const rememberMeCheckbox = document.getElementById('remember-me');
    if (savedEmail && loginEmailInput && rememberMeCheckbox) {
        loginEmailInput.value = savedEmail;
        rememberMeCheckbox.checked = true;
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async function (event) {
            event.preventDefault(); // Bloqueia o redirecionamento automático

            const email = document.getElementById('login-email')?.value;
            const password = document.getElementById('login-password')?.value;
            const rememberMe = document.getElementById('remember-me')?.checked;
            const submitBtn = this.querySelector('button[type="submit"]');

            if (submitBtn) submitBtn.disabled = true;

            try {
                const response = await fetch(`${API_URL}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                let data;
                try {
                    data = await response.json();
                } catch (parseError) {
                    console.error("Erro ao ler resposta do Python:", parseError);
                    throw new Error("O Python apresentou um erro interno. Verifique o terminal.");
                }

                if (response.ok) {
                    if (loginStatus) setFormStatus(loginStatus, data.message, 'success');

                    // Salva a sessão e o nome do usuário
                    if (data.token) {
                        localStorage.setItem('m2r_token', data.token);
                        localStorage.setItem('m2r_userName', data.nome);
                        document.cookie = `m2r_token=${data.token}; path=/; max-age=86400; Secure; SameSite=Lax`; // Salva no cookie
                    }

                    // Salva ou remove o e-mail dependendo da escolha
                    if (rememberMe) {
                        localStorage.setItem('m2r_saved_email', email);
                    } else {
                        localStorage.removeItem('m2r_saved_email');
                    }

                    // Sucesso! Libera o acesso para a página inicial
                    setTimeout(() => {
                        redirectBasedOnPath('index_inicio.html');
                    }, 1500);
                } else {
                    if (loginStatus) setFormStatus(loginStatus, data.error || 'E-mail ou senha incorretos.', 'error');
                }
            } catch (error) {
                console.error("Erro no fetch:", error);
                if (loginStatus) setFormStatus(loginStatus, error.message.includes('Python') ? error.message : `Falha de Conexão: ${error.message}`, 'error');
            } finally {
                if (submitBtn) submitBtn.disabled = false;
            }
        });
    }

    // --- Lógica de Mostrar/Ocultar Senha (Ícone de Olho) ---
    const setupPasswordToggle = (inputId, buttonId) => {
        const input = document.getElementById(inputId);
        const button = document.getElementById(buttonId);
        if (input && button) {
            button.addEventListener('click', () => {
                const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
                input.setAttribute('type', type);
                // Alterna o emoji dependendo do estado
                button.textContent = type === 'password' ? '👁️' : '🙈';
            });
        }
    };
    
    setupPasswordToggle('register-password', 'toggle-register-password');
    setupPasswordToggle('login-password', 'toggle-login-password');

    /*
        =====================================================
        10. ANIMAÇÃO DA COBRA SEGUINDO O MOUSE (TELA DE LOGIN)
        =====================================================
    */
    // Verifica se estamos na página de autenticação
    if (document.body.classList.contains('page-auth')) {
        // --- INICIALIZAÇÃO DO CANVAS DINÂMICO ---
        const canvas = document.createElement('canvas');
        canvas.id = 'snakeCanvas';
        canvas.style.position = 'absolute';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.zIndex = '0'; // Fica atrás do card de login
        canvas.style.opacity = '0'; // Começa invisível
        canvas.style.transition = 'opacity 1.5s ease-in-out'; // Fade-in suave ao aparecer
        canvas.style.pointerEvents = 'none'; // Permite clicar nos campos através do canvas

        // Anexa o canvas ao fundo da seção de login
        const loginSection = document.querySelector('.login-section');
        if (loginSection) {
            loginSection.appendChild(canvas);
        } else {
            document.body.appendChild(canvas);
        }

        const ctx = canvas.getContext('2d');
        let width, height;

        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = Math.max(window.innerHeight, loginSection ? loginSection.offsetHeight : document.documentElement.scrollHeight);
        }
        window.addEventListener('resize', resize);
        resize();

        // --- VARIÁVEIS DE CONTROLE ---
        const mouse = { x: width / 2, y: height / 2 };
        const prey = { x: width / 2 + 100, y: height / 2, angle: 0 };

        let hasMoved = false; // Variável para rastrear se o mouse se moveu

        window.addEventListener('mousemove', (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
            
            if (!hasMoved) {
                hasMoved = true;
                canvas.style.opacity = '1'; // A cobra e o rato aparecem suavemente ao mover o mouse
            }
        });

        // --- CONFIGURAÇÕES DA COBRA E DO RATO ---
        const numSegments = 100;
        const segmentLength = 5;
        const snakeSpeed = 0.05;
        const waveAmplitude = 2;
        const waveFrequency = 0.25;
        const waveSpeed = 0.05;
        
        let time = 0;
        const segments = [];

        for (let i = 0; i < numSegments; i++) {
            segments.push({ x: width / 2, y: height / 2, angle: 0 });
        }

        // --- LOOP DE ANIMAÇÃO ---
        function animate() {
            // Transparente para manter visível a grade e o gradiente do seu CSS de Login
            ctx.clearRect(0, 0, width, height);

            time += waveSpeed;

            // Se o mouse ainda não se moveu, paralisa a física e o desenho para economizar processamento
            if (!hasMoved) {
                requestAnimationFrame(animate);
                return;
            }

            // 1. Lógica do Rato
            const dxCursor = mouse.x - prey.x;
            const dyCursor = mouse.y - prey.y;
            const distCursor = Math.hypot(dxCursor, dyCursor);
            
            if (distCursor > 0.1) {
                prey.angle = Math.atan2(dyCursor, dxCursor);
                const preyMargin = 50;
                const preyError = distCursor - preyMargin;
                prey.x += Math.cos(prey.angle) * preyError * 0.15;
                prey.y += Math.sin(prey.angle) * preyError * 0.15;
            }

            // 2. Lógica da Cabeça da Cobra
            const head = segments[0];
            const dxPrey = prey.x - head.x;
            const dyPrey = prey.y - head.y;
            const distPrey = Math.hypot(dxPrey, dyPrey);
            
            if (distPrey > 0.1) {
                head.angle = Math.atan2(dyPrey, dxPrey);
                const snakeMargin = 80;
                const headError = distPrey - snakeMargin;
                head.x += Math.cos(head.angle) * headError * snakeSpeed;
                head.y += Math.sin(head.angle) * headError * snakeSpeed;
            }

            // 3. Lógica do Corpo
            for (let i = 1; i < numSegments; i++) {
                let current = segments[i];
                let prev = segments[i - 1];

                let dx = prev.x - current.x;
                let dy = prev.y - current.y;
                let angle = Math.atan2(dy, dx);
                current.angle = angle;

                let noMovementCount = Math.floor(numSegments / 18);
                let neckStiffness = 0;
                
                if (i > noMovementCount) {
                    neckStiffness = Math.min((i - noMovementCount) / 25, 1);
                }
                
                let slitherOffset = Math.sin(time - i * waveFrequency) * (waveAmplitude * neckStiffness);

                let targetX = prev.x - Math.cos(angle) * segmentLength;
                let targetY = prev.y - Math.sin(angle) * segmentLength;

                targetX += Math.cos(angle + Math.PI / 2) * slitherOffset;
                targetY += Math.sin(angle + Math.PI / 2) * slitherOffset;

                current.x += (targetX - current.x) * 0.40;
                current.y += (targetY - current.y) * 0.40;
            }

            // --- DESENHOS NO CANVAS ---

            // A. Desenhar o Rato
            ctx.save();
            ctx.translate(prey.x, prey.y);
            ctx.rotate(prey.angle);
            
            ctx.strokeStyle = '#555';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(-8, 0);
            ctx.quadraticCurveTo(-15, -6, -22, 0);
            ctx.stroke();

            ctx.fillStyle = '#888';
            ctx.beginPath();
            ctx.arc(3, -5, 3.5, 0, Math.PI * 2);
            ctx.arc(3, 5, 3.5, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#777';
            ctx.beginPath();
            ctx.ellipse(0, 0, 10, 5.5, 0, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#ff99aa';
            ctx.beginPath();
            ctx.arc(10, 0, 1.5, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();

            // B. Desenhar o Corpo da Cobra
            let neckLength = Math.floor(numSegments / 18);
            for (let i = numSegments - 1; i > 0; i--) {
                let current = segments[i];
                let size = 32;
                if (i > neckLength) {
                    let progress = (i - neckLength) / (numSegments - neckLength);
                    let easeProgress = Math.pow(progress, 0.8);
                    size = Math.max(4, 32 - (easeProgress * 28));
                }

                ctx.beginPath();
                ctx.arc(current.x, current.y, size / 2, 0, Math.PI * 2);
                
                if (i <= neckLength) {
                    ctx.fillStyle = '#c89a63';
                } else {
                    let progress = (i - neckLength) / (numSegments - neckLength);
                    let r = Math.round(200 - (200 - 90) * progress);
                    let g = Math.round(154 - (154 - 59) * progress);
                    let b = Math.round(99 - (99 - 32) * progress);
                    
                    let texture = i % 2 === 0 ? 0 : 10; 
                    ctx.fillStyle = `rgb(${r - texture}, ${g - texture}, ${b - texture})`;
                }
                ctx.fill();
            }

            // C. Desenhar a Cabeça da Cobra
            ctx.save();
            ctx.translate(head.x, head.y);
            ctx.rotate(head.angle);

            ctx.shadowColor = 'rgba(0, 0, 0, 0.7)';
            ctx.shadowBlur = 12;
            ctx.shadowOffsetY = 6;

            ctx.fillStyle = '#c89a63';
            ctx.beginPath();
            ctx.moveTo(24, 0);
            ctx.bezierCurveTo(20, 12, 5, 18, -6, 16);
            ctx.quadraticCurveTo(-12, 0, -6, -16);
            ctx.bezierCurveTo(5, -18, 20, -12, 24, 0);
            ctx.fill();

            ctx.fillStyle = '#111';
            ctx.beginPath();
            ctx.arc(8, -7, 2.5, 0, Math.PI * 2);
            ctx.arc(8, 7, 2.5, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#fff';
            ctx.beginPath();
            ctx.arc(8.5, -7.5, 0.8, 0, Math.PI * 2);
            ctx.arc(8.5, 7.5, 0.8, 0, Math.PI * 2);
            ctx.fill();

            let tongue = Math.sin(time * 3) * 8;
            if (tongue > 0) {
                ctx.strokeStyle = '#cc0000';
                ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.moveTo(24, 0);
                ctx.lineTo(24 + tongue, 0);
                ctx.lineTo(24 + tongue + 3, -3);
                ctx.moveTo(24 + tongue, 0);
                ctx.lineTo(24 + tongue + 3, 3);
                ctx.stroke();
            }
            ctx.restore();

            requestAnimationFrame(animate);
        }
        
        animate();
    }
}