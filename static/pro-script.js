/* ==========================================
   PROFESSIONAL INTERVIEW COACH - JAVASCRIPT
   ========================================== */

// -------- SMOOTH SCROLL & NAVIGATION --------

document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            link.classList.add('active');
        });
    });

    // Update active link on scroll
    window.addEventListener('scroll', () => {
        let current = '';
        const sections = document.querySelectorAll('section');

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.scrollY >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').slice(1) === current) {
                link.classList.add('active');
            }
        });
    });
});

// -------- SCROLL TO SECTIONS --------

function scrollToDemo() {
    const demoSection = document.getElementById('demo');
    if (demoSection) {
        demoSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function scrollToAuth() {
    const pricingSection = document.getElementById('pricing');
    if (pricingSection) {
        pricingSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// -------- PARALLAX EFFECT --------

window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.parallax-element');

    parallaxElements.forEach(element => {
        element.style.transform = `translateY(${scrolled * 0.5}px)`;
    });
});

// -------- INTERSECTION OBSERVER FOR ANIMATIONS --------

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = entry.target.dataset.animation || 'fade-in 0.6s ease-out';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all animated elements
document.querySelectorAll('[data-animation]').forEach(el => {
    observer.observe(el);
});

// -------- BUTTON HOVER EFFECTS --------

const buttons = document.querySelectorAll('.btn');

buttons.forEach(button => {
    button.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px)';
    });

    button.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });

    button.addEventListener('click', function(e) {
        // Create ripple effect
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');

        this.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    });
});

// -------- CARD HOVER LIFT --------

const cards = document.querySelectorAll('.feature-card, .pricing-card');

cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px)';
        this.style.boxShadow = '0 0 40px rgba(0, 102, 255, 0.4)';
    });

    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '';
    });
});

// -------- COUNTER ANIMATION --------

function animateCounter(element, target, duration = 2000) {
    let current = 0;
    const increment = target / (duration / 16);

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// -------- ANIMATE STATS ON SCROLL --------

const statsSection = document.querySelector('.hero-stats');
let statsAnimated = false;

window.addEventListener('scroll', () => {
    if (!statsAnimated && statsSection) {
        const rect = statsSection.getBoundingClientRect();
        if (rect.top < window.innerHeight) {
            const statNumbers = statsSection.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {
                const target = parseInt(stat.textContent.replace(/\D/g, ''));
                animateCounter(stat, target);
            });
            statsAnimated = true;
        }
    }
});

// -------- FLOATING ELEMENT ANIMATION --------

function createFloatingParticles() {
    const container = document.querySelector('.hero');
    if (!container) return;

    for (let i = 0; i < 5; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.style.width = Math.random() * 100 + 50 + 'px';
        particle.style.height = particle.style.width;
        particle.style.background = `rgba(0, ${Math.random() * 100 + 100}, 255, ${Math.random() * 0.1})`;
        particle.style.borderRadius = '50%';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.zIndex = '-1';
        particle.style.animation = `float ${Math.random() * 4 + 4}s ease-in-out infinite`;

        container.appendChild(particle);
    }
}

createFloatingParticles();

// -------- SMOOTH PAGE LOAD ANIMATION --------

window.addEventListener('load', () => {
    document.body.style.animation = 'fade-in 0.8s ease-out';
});

// -------- INTERACTIVE PROGRESS CIRCLE --------

const progressRing = document.querySelector('.progress-ring');
if (progressRing) {
    const radius = progressRing.r.baseVal.value;
    const circumference = radius * 2 * Math.PI;

    progressRing.style.strokeDasharray = circumference + ' ' + circumference;
    progressRing.style.strokeDashoffset = circumference;

    function setProgress(percent) {
        const offset = circumference - (percent / 100) * circumference;
        progressRing.style.strokeDashoffset = offset;
    }

    // Animate progress on load
    let progress = 0;
    const progressInterval = setInterval(() => {
        if (progress < 85) {
            progress += Math.random() * 30;
            setProgress(Math.min(progress, 85));
        } else {
            clearInterval(progressInterval);
            setProgress(85);
        }
    }, 300);
}

// -------- FORM VALIDATION & SUBMISSION --------

const forms = document.querySelectorAll('form');

forms.forEach(form => {
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // Show success message
        const successMsg = document.createElement('div');
        successMsg.textContent = '✓ Message sent successfully!';
        successMsg.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #00d084;
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            animation: slide-in-right 0.5s ease-out;
            z-index: 10000;
        `;

        document.body.appendChild(successMsg);

        setTimeout(() => {
            successMsg.style.animation = 'fade-out 0.5s ease-out';
            setTimeout(() => successMsg.remove(), 500);
        }, 3000);

        form.reset();
    });
});

// -------- CURSOR TRACKING EFFECT --------

document.addEventListener('mousemove', (e) => {
    const x = e.clientX;
    const y = e.clientY;

    // Create subtle glow effect at cursor for interactive elements
    const elements = document.querySelectorAll('.btn, .feature-card');

    elements.forEach(element => {
        const rect = element.getBoundingClientRect();
        const distance = Math.sqrt(
            Math.pow(x - (rect.left + rect.width / 2), 2) +
            Math.pow(y - (rect.top + rect.height / 2), 2)
        );

        if (distance < 200) {
            const opacity = 1 - distance / 200;
            element.style.boxShadow = `0 0 ${20 * opacity}px rgba(0, 102, 255, ${0.3 * opacity})`;
        }
    });
});

// -------- SCROLL REVEAL ANIMATION --------

const revealElements = document.querySelectorAll('.feature-card, .pricing-card, .step');

const scrollRevealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            scrollRevealObserver.unobserve(entry.target);
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
});

revealElements.forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(30px)';
    element.style.transition = 'all 0.6s ease-out';
    scrollRevealObserver.observe(element);
});

// -------- TYPING ANIMATION --------

function typeText(element, text, speed = 50) {
    let index = 0;
    element.textContent = '';

    function type() {
        if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            setTimeout(type, speed);
        }
    }

    type();
}

// -------- HIGHLIGHT TEXT ON HOVER --------

document.querySelectorAll('.section-title').forEach(title => {
    title.addEventListener('mouseenter', function() {
        this.style.textShadow = '0 0 20px rgba(0, 217, 255, 0.6)';
    });

    title.addEventListener('mouseleave', function() {
        this.style.textShadow = 'none';
    });
});

// -------- RESPONSIVE NAVIGATION TOGGLE --------

const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });

    // Close menu on link click
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
        });
    });
}

// -------- LAZY LOAD IMAGES --------

const images = document.querySelectorAll('img[data-src]');

const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
            imageObserver.unobserve(img);
        }
    });
});

images.forEach(img => imageObserver.observe(img));

// -------- RANDOM ANIMATION ON PAGE LOAD --------

window.addEventListener('load', () => {
    const elements = document.querySelectorAll('.feature-card, .step');
    elements.forEach((element, index) => {
        element.style.animationDelay = `${index * 0.1}s`;
        element.classList.add('animate-slide-in-up');
    });
});

console.log('✨ Coach.AI Premium Interface Loaded ✨');