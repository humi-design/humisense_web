/**
 * HUMISENSE - Premium JavaScript
 * GSAP Animations, Lenis Smooth Scroll, and Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    // ============================================
    // Loading Screen
    // ============================================
    const loader = document.getElementById('loader');
    if (loader) {
        setTimeout(() => {
            loader.classList.add('hidden');
        }, 1500);
    }

    // ============================================
    // Lenis Smooth Scroll
    // ============================================
    if (typeof Lenis !== 'undefined') {
        const lenis = new Lenis({
            duration: 1.2,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            orientation: 'vertical',
            gestureOrientation: 'vertical',
            smoothWheel: true,
            wheelMultiplier: 1,
            touchMultiplier: 2,
            infinite: false,
        });

        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);

        // Integrate with GSAP ScrollTrigger
        lenis.on('scroll', ScrollTrigger.update);
        gsap.ticker.add((time) => {
            lenis.raf(time * 1000);
        });
        gsap.ticker.lagSmoothing(0);
    }

    // ============================================
    // GSAP Animations
    // ============================================
    gsap.registerPlugin(ScrollTrigger);

    // Animate elements on scroll
    const animateElements = document.querySelectorAll('[data-animate]');
    animateElements.forEach((el) => {
        const delay = parseFloat(el.dataset.delay) || 0;
        
        gsap.fromTo(el, 
            { 
                opacity: 0, 
                y: 30 
            },
            {
                opacity: 1,
                y: 0,
                duration: 0.8,
                delay: delay / 1000,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: el,
                    start: 'top 85%',
                    toggleActions: 'play none none none'
                }
            }
        );
    });

    // Stagger children animations
    const staggerContainers = document.querySelectorAll('.stagger-children');
    staggerContainers.forEach((container) => {
        const children = container.children;
        
        gsap.fromTo(children, 
            { 
                opacity: 0, 
                y: 30 
            },
            {
                opacity: 1,
                y: 0,
                duration: 0.6,
                stagger: 0.1,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: container,
                    start: 'top 80%',
                    toggleActions: 'play none none none'
                }
            }
        );
    });

    // ============================================
    // Counter Animations
    // ============================================
    const counters = document.querySelectorAll('.counter');
    counters.forEach((counter) => {
        const target = parseInt(counter.dataset.target);
        const duration = 2;
        
        ScrollTrigger.create({
            trigger: counter,
            start: 'top 85%',
            onEnter: () => {
                gsap.to(counter, {
                    innerText: target,
                    duration: duration,
                    ease: 'power2.out',
                    snap: { innerText: 1 },
                    onUpdate: function() {
                        counter.innerText = Math.round(this.targets()[0].innerText);
                    }
                });
            },
            once: true
        });
    });

    // ============================================
    // FAQ Accordion
    // ============================================
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach((item) => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        
        question?.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Close all other items
            faqItems.forEach((otherItem) => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                    const otherAnswer = otherItem.querySelector('.faq-answer');
                    if (otherAnswer) {
                        gsap.to(otherAnswer, {
                            maxHeight: 0,
                            duration: 0.3,
                            ease: 'power2.inOut'
                        });
                    }
                }
            });
            
            // Toggle current item
            if (isActive) {
                item.classList.remove('active');
                gsap.to(answer, {
                    maxHeight: 0,
                    duration: 0.3,
                    ease: 'power2.inOut'
                });
            } else {
                item.classList.add('active');
                gsap.fromTo(answer, 
                    { maxHeight: 0 },
                    {
                        maxHeight: 500,
                        duration: 0.4,
                        ease: 'power2.out'
                    }
                );
            }
        });
    });

    // ============================================
    // Tabs
    // ============================================
    const tabContainers = document.querySelectorAll('.tabs');
    tabContainers.forEach((container) => {
        const tabs = container.querySelectorAll('.tab');
        const parent = container.parentElement;
        const contents = parent?.querySelectorAll('.tab-content');
        
        tabs.forEach((tab) => {
            tab.addEventListener('click', () => {
                const targetId = tab.dataset.tab;
                
                // Update active tab
                tabs.forEach((t) => t.classList.remove('active'));
                tab.classList.add('active');
                
                // Show corresponding content
                contents?.forEach((content) => {
                    if (content.id === targetId) {
                        content.classList.add('active');
                        gsap.fromTo(content, 
                            { opacity: 0, y: 20 },
                            { opacity: 1, y: 0, duration: 0.3 }
                        );
                    } else {
                        content.classList.remove('active');
                    }
                });
            });
        });
    });

    // ============================================
    // Scroll to Top Button
    // ============================================
    const scrollTopBtn = document.getElementById('scrollTop');
    
    if (scrollTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 500) {
                scrollTopBtn.classList.add('visible');
            } else {
                scrollTopBtn.classList.remove('visible');
            }
        });
        
        scrollTopBtn.addEventListener('click', () => {
            if (typeof Lenis !== 'undefined') {
                lenis.scrollTo(0, { duration: 1.5 });
            } else {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    }

    // ============================================
    // Magnetic Button Effect
    // ============================================
    const magneticButtons = document.querySelectorAll('.magnetic-btn');
    
    magneticButtons.forEach((btn) => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            gsap.to(btn, {
                x: x * 0.2,
                y: y * 0.2,
                duration: 0.3,
                ease: 'power2.out'
            });
        });
        
        btn.addEventListener('mouseleave', () => {
            gsap.to(btn, {
                x: 0,
                y: 0,
                duration: 0.5,
                ease: 'elastic.out(1, 0.5)'
            });
        });
    });

    // ============================================
    // Card Hover Effects
    // ============================================
    const cards = document.querySelectorAll('.product-card, .service-card, .course-card, .agent-card, .testimonial-card');
    
    cards.forEach((card) => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, {
                y: -8,
                duration: 0.3,
                ease: 'power2.out'
            });
        });
        
        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                y: 0,
                duration: 0.5,
                ease: 'elastic.out(1, 0.5)'
            });
        });
    });

    // ============================================
    // Code Copy Button
    // ============================================
    const copyButtons = document.querySelectorAll('.code-copy');
    
    copyButtons.forEach((btn) => {
        btn.addEventListener('click', async () => {
            const codeBlock = btn.closest('.code-block');
            const code = codeBlock?.querySelector('pre')?.textContent;
            
            if (code) {
                try {
                    await navigator.clipboard.writeText(code);
                    btn.textContent = 'Copied!';
                    setTimeout(() => {
                        btn.textContent = 'Copy';
                    }, 2000);
                } catch (err) {
                    console.error('Failed to copy:', err);
                }
            }
        });
    });

    // ============================================
    // Form Validation with JustValidate
    // ============================================
    if (typeof JustValidate !== 'undefined') {
        const contactForm = document.querySelector('#contact-form');
        
        if (contactForm) {
            new JustValidate(contactForm, {
                rules: {
                    name: {
                        required: true,
                        minLength: 2
                    },
                    email: {
                        required: true,
                        email: true
                    },
                    subject: {
                        required: true
                    },
                    message: {
                        required: true,
                        minLength: 10
                    }
                },
                messages: {
                    name: {
                        required: 'Name is required',
                        minLength: 'Name must be at least 2 characters'
                    },
                    email: {
                        required: 'Email is required',
                        email: 'Please enter a valid email'
                    },
                    subject: {
                        required: 'Please select a subject'
                    },
                    message: {
                        required: 'Message is required',
                        minLength: 'Message must be at least 10 characters'
                    }
                },
                submitHandler: function(form, values) {
                    // Form submission will be handled by Flask
                    form.submit();
                }
            });
        }
    }

    // ============================================
    // Parallax Effects
    // ============================================
    const parallaxElements = document.querySelectorAll('.hero-gradient, .cta-gradient');
    
    parallaxElements.forEach((el) => {
        gsap.to(el, {
            y: -100,
            ease: 'none',
            scrollTrigger: {
                trigger: el.parentElement,
                start: 'top top',
                end: 'bottom top',
                scrub: 1
            }
        });
    });

    // ============================================
    // Link Hover Effects
    // ============================================
    const links = document.querySelectorAll('.product-link, .nav-link');
    
    links.forEach((link) => {
        link.addEventListener('mouseenter', () => {
            gsap.to(link, {
                x: 4,
                duration: 0.2,
                ease: 'power2.out'
            });
        });
        
        link.addEventListener('mouseleave', () => {
            gsap.to(link, {
                x: 0,
                duration: 0.3,
                ease: 'power2.out'
            });
        });
    });

    // ============================================
    // Page Transition
    // ============================================
    const links_internal = document.querySelectorAll('a[href^="/"]');
    
    links_internal.forEach((link) => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href && !href.startsWith('#')) {
                e.preventDefault();
                
                gsap.to('body', {
                    opacity: 0,
                    duration: 0.3,
                    ease: 'power2.inOut',
                    onComplete: () => {
                        window.location.href = href;
                    }
                });
            }
        });
    });

    // ============================================
    // Hero Text Animation
    // ============================================
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const lines = heroTitle.querySelectorAll('.hero-title-line');
        
        gsap.fromTo(lines, 
            { 
                opacity: 0, 
                y: 50 
            },
            {
                opacity: 1,
                y: 0,
                duration: 1,
                stagger: 0.2,
                ease: 'power3.out',
                delay: 0.5
            }
        );
    }

    // ============================================
    // Gradient Text Animation
    // ============================================
    const gradientTexts = document.querySelectorAll('.gradient-text');
    
    gradientTexts.forEach((text) => {
        gsap.fromTo(text, 
            { 
                backgroundPosition: '0% 50%' 
            },
            {
                backgroundPosition: '100% 50%',
                duration: 3,
                ease: 'power1.inOut',
                repeat: -1,
                yoyo: true
            }
        );
    });

    // ============================================
    // Button Ripple Effect
    // ============================================
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.style.cssText = `
                position: absolute;
                width: 100px;
                height: 100px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: translate(-50%, -50%) scale(0);
                pointer-events: none;
                left: ${x}px;
                top: ${y}px;
            `;
            
            btn.style.position = 'relative';
            btn.style.overflow = 'hidden';
            btn.appendChild(ripple);
            
            gsap.to(ripple, {
                scale: 4,
                opacity: 0,
                duration: 0.6,
                ease: 'power2.out',
                onComplete: () => {
                    ripple.remove();
                }
            });
        });
    });

    // ============================================
    // Swiper Carousel (if needed)
    // ============================================
    if (typeof Swiper !== 'undefined') {
        const testimonialSwiper = new Swiper('.testimonial-swiper', {
            slidesPerView: 1,
            spaceBetween: 30,
            loop: true,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            breakpoints: {
                640: {
                    slidesPerView: 2,
                },
                1024: {
                    slidesPerView: 3,
                },
            },
        });
    }

    console.log('HUMISENSE Premium JS initialized');
});