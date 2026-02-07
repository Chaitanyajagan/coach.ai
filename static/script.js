// ============================================
// DOM ELEMENTS
// ============================================

const navMenu = document.getElementById('navMenu');
const hamburger = document.getElementById('hamburger');
const navLinks = document.querySelectorAll('.nav-link');
const authTabBtns = document.querySelectorAll('.auth-tab-btn');
const authTabs = document.querySelectorAll('.auth-tab');

// ============================================
// HAMBURGER MENU
// ============================================

hamburger.addEventListener('click', () => {
    navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
});

// Close menu when link is clicked
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.style.display = 'none';
    });
});

// ============================================
// NAVIGATION ACTIVE LINK
// ============================================

const observerOptions = {
    threshold: 0.3
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const id = entry.target.id;
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${id}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}, observerOptions);

// Observe all sections
document.querySelectorAll('section').forEach(section => {
    observer.observe(section);
});

// ============================================
// AUTH TABS
// ============================================

authTabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        
        // Remove active from all tabs
        authTabs.forEach(tab => {
            tab.classList.remove('active');
        });
        authTabBtns.forEach(b => {
            b.classList.remove('active');
        });
        
        // Add active to clicked tab
        btn.classList.add('active');
        document.getElementById(`${tabName}-tab`).classList.add('active');
    });
});

// ============================================
// SCROLL ANIMATIONS
// ============================================

const animateOnScroll = () => {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    const observerScroll = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                observerScroll.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    elements.forEach(el => {
        observerScroll.observe(el);
    });
};

// Call animation on page load
window.addEventListener('load', animateOnScroll);

// ============================================
// SMOOTH SCROLL TO AUTH
// ============================================

function scrollToAuth() {
    const authSection = document.getElementById('auth');
    authSection.scrollIntoView({ behavior: 'smooth' });
}

// ============================================
// FORM VALIDATION
// ============================================

const loginForm = document.querySelector('#login-tab .auth-form');
const signupForm = document.querySelector('#signup-tab .auth-form');

if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        
        if (validateEmail(email) && password.length >= 6) {
            console.log('Login submitted:', { email, password });
            showNotification('Login successful! Redirecting...', 'success');
            // Redirect to app after 2 seconds
            setTimeout(() => {
                window.location.href = 'http://localhost:8501';
            }, 2000);
        } else {
            showNotification('Please enter valid credentials', 'error');
        }
    });
}

if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('signup-name').value;
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;
        
        if (name && validateEmail(email) && password.length >= 6) {
            console.log('Signup submitted:', { name, email, password });
            showNotification('Account created successfully!', 'success');
            setTimeout(() => {
                // Switch to login tab
                document.querySelector('[data-tab="login"]').click();
            }, 1500);
        } else {
            showNotification('Please fill in all fields correctly', 'error');
        }
    });
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#6366f1'};
        color: white;
        border-radius: 8px;
        font-weight: 600;
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideInRight 0.3s ease-out reverse';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// ============================================
// PASSWORD STRENGTH INDICATOR
// ============================================

const signupPassword = document.getElementById('signup-password');
if (signupPassword) {
    signupPassword.addEventListener('input', () => {
        const password = signupPassword.value;
        const strengthBar = signupPassword.parentElement.querySelector('.strength-bar');
        const strengthText = signupPassword.parentElement.querySelector('.strength-text');
        
        let strength = 0;
        if (password.length >= 6) strength++;
        if (password.length >= 10) strength++;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^a-zA-Z0-9]/.test(password)) strength++;
        
        const strengthPercentage = (strength / 5) * 100;
        const after = strengthBar.querySelector('::after');
        
        if (after) {
            after.style.width = strengthPercentage + '%';
        }
        
        if (strength <= 2) {
            strengthText.textContent = 'Weak';
            strengthText.style.color = '#ef4444';
        } else if (strength <= 3) {
            strengthText.textContent = 'Medium';
            strengthText.style.color = '#f59e0b';
        } else {
            strengthText.textContent = 'Strong';
            strengthText.style.color = '#10b981';
        }
    });
}

// ============================================
// PARALLAX EFFECT
// ============================================

window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const heroGradient = document.querySelector('.hero-gradient');
    
    if (heroGradient) {
        heroGradient.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// ============================================
// BUTTON RIPPLE EFFECT
// ============================================

document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const ripple = document.createElement('span');
        ripple.style.cssText = `
            position: absolute;
            width: 20px;
            height: 20px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            left: ${x}px;
            top: ${y}px;
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        `;
        
        this.style.position = 'relative';
        this.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    });
});

// Add ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple-animation {
        to {
            width: 200px;
            height: 200px;
            opacity: 0;
            transform: translate(-50%, -50%);
        }
    }
`;
document.head.appendChild(style);

// ============================================
// CURSOR TRACKING
// ============================================

document.addEventListener('mousemove', (e) => {
    const cards = document.querySelectorAll('.feature-card, .pricing-card');
    
    cards.forEach(card => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left - rect.width / 2) / 10;
        const y = (e.clientY - rect.top - rect.height / 2) / 10;
        
        card.style.transform = `perspective(1000px) rotateX(${y}deg) rotateY(${x}deg)`;
    });
});

// Reset on mouse leave
document.addEventListener('mouseleave', () => {
    const cards = document.querySelectorAll('.feature-card, .pricing-card');
    cards.forEach(card => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';
    });
});

// ============================================
// PAGE LOAD ANIMATION
// ============================================

window.addEventListener('load', () => {
    document.body.style.opacity = '1';
    animateOnScroll();
});

// ============================================
// INTERSECTION OBSERVER FOR COUNTERS
// ============================================

function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start);
        }
    }, 16);
}

// ============================================
// MOBILE MENU CLOSE ON OUTSIDE CLICK
// ============================================

document.addEventListener('click', (e) => {
    if (!e.target.closest('.navbar')) {
        navMenu.style.display = 'none';
    }
});

// ============================================
// PREVENT RIGHT CLICK FOR PRODUCTION
// ============================================

// Uncomment for production
// document.addEventListener('contextmenu', e => e.preventDefault());