/* =====================================================
   HUMISENSE - Premium JavaScript
   GSAP, Lenis, Three.js, and advanced interactions
   ===================================================== */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', () => {
    'use strict';

    // =====================================================
    // CONFIGURATION
    // =====================================================
    const CONFIG = {
        // Animation timing
        animation: {
            defaultDuration: 0.8,
            staggerDelay: 0.1,
            scrollTriggerStart: 'top 80%',
            scrollTriggerEnd: 'bottom 20%',
        },
        // Parallax settings
        parallax: {
            strength: 0.1,
            smooth: 0.1,
        },
        // Cursor settings
        cursor: {
            size: 20,
            followerSize: 8,
            smoothing: 0.15,
        },
        // Lenis smooth scroll
        lenis: {
            duration: 1.2,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            orientation: 'vertical',
            smoothWheel: true,
        },
    };

    // =====================================================
    // GLOBAL STATE
    // =====================================================
    let lenis = null;
    let gsapContext = null;
    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;
    let scrollY = 0;

    // =====================================================
    // LOADER
    // =====================================================
    function initLoader() {
        const loader = document.querySelector('.loader');
        if (!loader) return;

        // Hide loader after animations complete
        window.addEventListener('load', () => {
            gsap.to(loader, {
                opacity: 0,
                duration: 0.5,
                delay: 1.5,
                onComplete: () => {
                    loader.classList.add('hidden');
                    document.body.style.overflow = '';
                }
            });
        });
    }

    // =====================================================
    // LENIS SMOOTH SCROLL
    // =====================================================
    function initLenis() {
        if (typeof Lenis === 'undefined') {
            console.warn('Lenis not loaded');
            return;
        }

        lenis = new Lenis({
            duration: CONFIG.lenis.duration,
            easing: CONFIG.lenis.easing,
            orientation: CONFIG.lenis.orientation,
            smoothWheel: CONFIG.lenis.smoothWheel,
        });

        // Connect Lenis to GSAP ScrollTrigger
        lenis.on('scroll', ScrollTrigger.update);

        gsap.ticker.add((time) => {
            lenis.raf(time * 1000);
        });

        gsap.ticker.lagSmoothing(0);

        // Expose lenis globally for use
        window.lenis = lenis;
    }

    // =====================================================
    // GSAP SCROLL ANIMATIONS
    // =====================================================
    function initScrollAnimations() {
        gsap.registerPlugin(ScrollTrigger);

        gsapContext = gsap.context(() => {
            // Animate elements with data-animate attribute
            gsap.utils.toArray('[data-animate]').forEach((el) => {
                const delay = parseFloat(el.dataset.delay) || 0;
                const x = el.dataset.animateLeft ? -60 : el.dataset.animateRight ? 60 : 0;
                const y = el.dataset.animateUp ? 60 : el.dataset.animateDown ? -60 : 0;
                const scale = el.dataset.animateScale ? 0.8 : 1;

                gsap.from(el, {
                    opacity: 0,
                    x, y,
                    scale,
                    duration: CONFIG.animation.defaultDuration,
                    delay,
                    ease: 'power3.out',
                    scrollTrigger: {
                        trigger: el,
                        start: CONFIG.animation.scrollTriggerStart,
                        toggleActions: 'play none none none',
                    }
                });
            });

            // Fade in up animation for sections
            gsap.utils.toArray('.fade-in-up').forEach((section) => {
                const children = section.querySelectorAll('.animate-item');
                if (children.length) {
                    gsap.from(children, {
                        opacity: 0,
                        y: 40,
                        duration: 0.8,
                        stagger: CONFIG.animation.staggerDelay,
                        ease: 'power3.out',
                        scrollTrigger: {
                            trigger: section,
                            start: CONFIG.animation.scrollTriggerStart,
                        }
                    });
                }
            });

            // Stagger children animation
            gsap.utils.toArray('.stagger-children').forEach((container) => {
                const children = container.children;
                gsap.from(children, {
                    opacity: 0,
                    y: 30,
                    duration: 0.6,
                    stagger: 0.1,
                    ease: 'power3.out',
                    scrollTrigger: {
                        trigger: container,
                        start: CONFIG.animation.scrollTriggerStart,
                    }
                });
            });

            // Scale in animation
            gsap.utils.toArray('.scale-in').forEach((el) => {
                gsap.from(el, {
                    scale: 0.9,
                    opacity: 0,
                    duration: 0.8,
                    ease: 'power3.out',
                    scrollTrigger: {
                        trigger: el,
                        start: CONFIG.animation.scrollTriggerStart,
                    }
                });
            });

            // Text reveal animation
            gsap.utils.toArray('.text-reveal').forEach((text) => {
                gsap.from(text, {
                    y: '100%',
                    duration: 1,
                    ease: 'power4.out',
                    scrollTrigger: {
                        trigger: text,
                        start: CONFIG.animation.scrollTriggerStart,
                    }
                });
            });

            // Image reveal animation
            gsap.utils.toArray('.image-reveal').forEach((container) => {
                const img = container.querySelector('img');
                if (!img) return;

                gsap.from(img, {
                    scale: 1.2,
                    duration: 1.5,
                    ease: 'power3.out',
                    scrollTrigger: {
                        trigger: container,
                        start: CONFIG.animation.scrollTriggerStart,
                    }
                });
            });

            // Parallax effect
            gsap.utils.toArray('.parallax').forEach((el) => {
                const speed = parseFloat(el.dataset.speed) || 0.1;
                gsap.to(el, {
                    y: () => -scrollY * speed,
                    ease: 'none',
                    scrollTrigger: {
                        trigger: el,
                        start: 'top bottom',
                        end: 'bottom top',
                        scrub: true,
                    }
                });
            });

            // Counter animation
            gsap.utils.toArray('.counter').forEach((counter) => {
                const target = parseInt(counter.dataset.target) || 0;
                const suffix = counter.dataset.suffix || '';
                const prefix = counter.dataset.prefix || '';
                const duration = 2;

                gsap.fromTo(counter, 
                    { innerText: 0 },
                    {
                        innerText: target,
                        duration,
                        ease: 'power2.out',
                        snap: { innerText: 1 },
                        scrollTrigger: {
                            trigger: counter,
                            start: CONFIG.animation.scrollTriggerStart,
                        },
                        onUpdate: function() {
                            counter.innerText = prefix + Math.round(this.targets()[0].innerText) + suffix;
                        }
                    }
                );
            });

            // Horizontal scroll section
            const horizontalSections = document.querySelectorAll('.horizontal-scroll-section');
            horizontalSections.forEach((section) => {
                const scrollContainer = section.querySelector('.horizontal-scroll');
                const scrollWidth = scrollContainer.scrollWidth - section.offsetWidth;

                gsap.to(scrollContainer, {
                    x: -scrollWidth,
                    ease: 'none',
                    scrollTrigger: {
                        trigger: section,
                        start: 'top top',
                        end: () => `+=${scrollWidth}`,
                        pin: true,
                        scrub: 1,
                        anticipatePin: 1,
                    }
                });
            });

        });

        // Refresh ScrollTrigger on resize
        window.addEventListener('resize', () => {
            ScrollTrigger.refresh();
        });
    }

    // =====================================================
    // INTERSECTION OBSERVER FOR ANIMATIONS
    // =====================================================
    function initIntersectionObserver() {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1,
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    
                    // Optional: unobserve after animation triggers once
                    // observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observe elements
        document.querySelectorAll('.fade-in-up, .scale-in, .stagger-children').forEach((el) => {
            observer.observe(el);
        });
    }

    // =====================================================
    // CURSOR EFFECTS
    // =====================================================
    function initCursor() {
        // Only enable on desktop
        if (window.innerWidth < 992 || 'ontouchstart' in window) return;

        let cursor = document.querySelector('.cursor');
        let cursorFollower = document.querySelector('.cursor-follower');

        if (!cursor) {
            cursor = document.createElement('div');
            cursor.className = 'cursor';
            document.body.appendChild(cursor);
        }

        if (!cursorFollower) {
            cursorFollower = document.createElement('div');
            cursorFollower.className = 'cursor-follower';
            document.body.appendChild(cursorFollower);
        }

        // Mouse move handler
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        // Animate cursor
        function animateCursor() {
            cursorX += (mouseX - cursorX) * CONFIG.cursor.smoothing;
            cursorY += (mouseY - cursorY) * CONFIG.cursor.smoothing;

            cursor.style.left = mouseX - CONFIG.cursor.size / 2 + 'px';
            cursor.style.top = mouseY - CONFIG.cursor.size / 2 + 'px';

            cursorFollower.style.left = cursorX - CONFIG.cursor.followerSize / 2 + 'px';
            cursorFollower.style.top = cursorY - CONFIG.cursor.followerSize / 2 + 'px';

            requestAnimationFrame(animateCursor);
        }
        animateCursor();

        // Hover effects for interactive elements
        const interactiveElements = document.querySelectorAll('a, button, .card, .product-card');
        interactiveElements.forEach((el) => {
            el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
            el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
        });
    }

    // =====================================================
    // MAGNETIC BUTTON EFFECT
    // =====================================================
    function initMagneticButtons() {
        const magneticBtns = document.querySelectorAll('.magnetic-btn');

        magneticBtns.forEach((btn) => {
            const content = btn.querySelector('.btn-content') || btn;

            btn.addEventListener('mousemove', (e) => {
                const rect = btn.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;

                gsap.to(content, {
                    x: x * 0.3,
                    y: y * 0.3,
                    duration: 0.3,
                    ease: 'power2.out',
                });
            });

            btn.addEventListener('mouseleave', () => {
                gsap.to(content, {
                    x: 0,
                    y: 0,
                    duration: 0.5,
                    ease: 'elastic.out(1, 0.5)',
                });
            });
        });
    }

    // =====================================================
    // 3D TILT CARD EFFECT
    // =====================================================
    function initTiltCards() {
        const tiltCards = document.querySelectorAll('.tilt-card-3d');

        tiltCards.forEach((card) => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;

                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;

                // Update CSS variable for glow position
                const percentX = (x / rect.width) * 100;
                const percentY = (y / rect.height) * 100;
                card.style.setProperty('--mouse-x', `${percentX}%`);
                card.style.setProperty('--mouse-y', `${percentY}%`);
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
            });
        });
    }

    // =====================================================
    // FAQ ACCORDION
    // =====================================================
    function initFAQ() {
        const faqItems = document.querySelectorAll('.faq-item');

        faqItems.forEach((item) => {
            const question = item.querySelector('.faq-question');
            const answer = item.querySelector('.faq-answer');

            question.addEventListener('click', () => {
                const isActive = item.classList.contains('active');

                // Close all other items
                faqItems.forEach((otherItem) => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                        otherItem.querySelector('.faq-answer').style.maxHeight = '0';
                    }
                });

                // Toggle current item
                if (isActive) {
                    item.classList.remove('active');
                    answer.style.maxHeight = '0';
                } else {
                    item.classList.add('active');
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                }
            });
        });
    }

    // =====================================================
    // SPOTLIGHT EFFECT
    // =====================================================
    function initSpotlight() {
        const spotlight = document.querySelector('.spotlight');
        if (!spotlight) return;

        document.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth) * 100;
            const y = (e.clientY / window.innerHeight) * 100;
            spotlight.style.setProperty('--mouse-x', `${x}%`);
            spotlight.style.setProperty('--mouse-y', `${y}%`);
        });
    }

    // =====================================================
    // SCROLL PROGRESS BAR
    // =====================================================
    function initScrollProgress() {
        const progressBar = document.querySelector('.scroll-progress');
        if (!progressBar) return;

        window.addEventListener('scroll', () => {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const progress = (scrollTop / docHeight) * 100;
            progressBar.style.width = `${progress}%`;
        });
    }

    // =====================================================
    // NAVBAR SCROLL EFFECT
    // =====================================================
    function initNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        if (!navbar) return;

        let lastScroll = 0;

        window.addEventListener('scroll', () => {
            const currentScroll = window.scrollY;

            if (currentScroll > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            lastScroll = currentScroll;
        });
    }

    // =====================================================
    // RIPPLE EFFECT FOR BUTTONS
    // =====================================================
    function initRipple() {
        const rippleBtns = document.querySelectorAll('.btn-ripple');

        rippleBtns.forEach((btn) => {
            btn.addEventListener('click', (e) => {
                const rect = btn.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const ripple = document.createElement('span');
                ripple.className = 'ripple-effect';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';

                btn.appendChild(ripple);

                setTimeout(() => ripple.remove(), 600);
            });
        });
    }

    // =====================================================
    // TESTIMONIALS AUTO-SCROLL
    // =====================================================
    function initTestimonialsScroll() {
        const track = document.querySelector('.testimonials-track');
        if (!track) return;

        // Duplicate items for infinite scroll
        const items = track.innerHTML;
        track.innerHTML = items + items;
    }

    // =====================================================
    // SMOOTH ANCHOR SCROLLING
    // =====================================================
    function initSmoothAnchors() {
        document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
            anchor.addEventListener('click', (e) => {
                const href = anchor.getAttribute('href');
                if (href === '#') return;

                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    
                    if (lenis) {
                        lenis.scrollTo(target, { offset: -80 });
                    } else {
                        target.scrollIntoView({ behavior: 'smooth' });
                    }
                }
            });
        });
    }

    // =====================================================
    // LAZY LOADING IMAGES
    // =====================================================
    function initLazyLoading() {
        if ('loading' in HTMLImageElement.prototype) {
            // Native lazy loading supported
            document.querySelectorAll('img[data-src]').forEach((img) => {
                img.src = img.dataset.src;
            });
        } else {
            // Fallback to Intersection Observer
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.add('loaded');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach((img) => {
                imageObserver.observe(img);
            });
        }
    }

    // =====================================================
    // SCROLL TRIGGERED REVEAL
    // =====================================================
    function initScrollReveal() {
        const revealElements = document.querySelectorAll('.reveal-clip, .reveal-blur');

        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });

        revealElements.forEach((el) => revealObserver.observe(el));
    }

    // =====================================================
    // MOBILE MENU TOGGLE
    // =====================================================
    function initMobileMenu() {
        const menuToggle = document.querySelector('.mobile-menu-toggle');
        const mobileMenu = document.querySelector('.mobile-menu');
        const menuOverlay = document.querySelector('.menu-overlay');

        if (!menuToggle || !mobileMenu) return;

        const toggleMenu = () => {
            const isOpen = mobileMenu.classList.contains('open');
            
            mobileMenu.classList.toggle('open');
            menuOverlay?.classList.toggle('open');
            document.body.style.overflow = isOpen ? '' : 'hidden';

            // Animate hamburger to X
            const lines = menuToggle.querySelectorAll('span');
            if (!isOpen) {
                gsap.to(lines[0], { rotation: 45, y: 6, duration: 0.3 });
                gsap.to(lines[1], { opacity: 0, duration: 0.3 });
                gsap.to(lines[2], { rotation: -45, y: -6, duration: 0.3 });
            } else {
                gsap.to(lines[0], { rotation: 0, y: 0, duration: 0.3 });
                gsap.to(lines[1], { opacity: 1, duration: 0.3 });
                gsap.to(lines[2], { rotation: 0, y: 0, duration: 0.3 });
            }
        };

        menuToggle.addEventListener('click', toggleMenu);
        menuOverlay?.addEventListener('click', toggleMenu);

        // Close on link click
        mobileMenu.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', () => {
                if (mobileMenu.classList.contains('open')) {
                    toggleMenu();
                }
            });
        });
    }

    // =====================================================
    // SCROLL LINK ACTIVE STATE
    // =====================================================
    function initScrollSpy() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

        const observerOptions = {
            rootMargin: '-20% 0px -80% 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    navLinks.forEach((link) => {
                        link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
                    });
                }
            });
        }, observerOptions);

        sections.forEach((section) => observer.observe(section));
    }

    // =====================================================
    // PARTICLE GENERATOR
    // =====================================================
    function initParticles() {
        const particleContainers = document.querySelectorAll('.particles');

        particleContainers.forEach((container) => {
            const count = parseInt(container.dataset.count) || 50;
            const colors = container.dataset.colors?.split(',') || ['#6366f1', '#8b5cf6', '#06b6d4'];

            for (let i = 0; i < count; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
                particle.style.animationDelay = (Math.random() * 10) + 's';
                particle.style.background = colors[Math.floor(Math.random() * colors.length)];
                particle.style.width = (Math.random() * 4 + 2) + 'px';
                particle.style.height = particle.style.width;
                container.appendChild(particle);
            }
        });
    }

    // =====================================================
    // PRELOAD CRITICAL ASSETS
    // =====================================================
    function preloadAssets() {
        // Preload fonts
        const fonts = [
            'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap',
        ];

        fonts.forEach((font) => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'style';
            link.href = font;
            document.head.appendChild(link);
        });
    }

    // =====================================================
    // PERFORMANCE: THROTTLE SCROLL EVENTS
    // =====================================================
    function throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // =====================================================
    // INITIALIZE ALL
    // =====================================================
    function init() {
        // Show loading state
        document.body.style.overflow = 'hidden';

        // Initialize components
        initLoader();
        initLenis();
        initScrollAnimations();
        initIntersectionObserver();
        initCursor();
        initMagneticButtons();
        initTiltCards();
        initFAQ();
        initSpotlight();
        initScrollProgress();
        initNavbarScroll();
        initRipple();
        initTestimonialsScroll();
        initSmoothAnchors();
        initLazyLoading();
        initScrollReveal();
        initMobileMenu();
        initScrollSpy();
        initParticles();
        preloadAssets();

        // Refresh on complete
        window.addEventListener('load', () => {
            ScrollTrigger.refresh();
        });
    }

    // Run initialization
    init();

    // =====================================================
    // EXPORT FOR EXTERNAL USE
    // =====================================================
    window.HumisenseUI = {
        lenis,
        gsap,
        ScrollTrigger,
        refresh: () => {
            ScrollTrigger.refresh();
            lenis?.resize();
        }
    };
});