/**
 * YoSiDi CAD - Landing Page Main JavaScript
 * Handles scroll animations, carousel, and interactive features
 */

// ========================================
// DOM Ready
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    initScrollAnimations();
    initCarousel();
    initSmoothScroll();
    initCountriesCounter();
    setCurrentYear();
});

// ========================================
// Scroll Animations
// ========================================
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add staggered delay for feature cards
                setTimeout(() => {
                    entry.target.classList.add('animate');
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        observer.observe(card);
    });

    // Observe all workflow steps
    const workflowSteps = document.querySelectorAll('.workflow-step');
    workflowSteps.forEach(step => {
        observer.observe(step);
    });
}

// ========================================
// Countries Counter Animation
// ========================================
function initCountriesCounter() {
    const counterElement = document.querySelector('.countries-number');
    if (!counterElement) return;

    const target = parseInt(counterElement.getAttribute('data-target'), 10);
    const duration = 2000;
    const startTime = performance.now();
    let hasAnimated = false;

    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !hasAnimated) {
                hasAnimated = true;
                animateCounter();
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    observer.observe(counterElement);

    function animateCounter() {
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(easeOut * target);

            counterElement.textContent = current;

            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                counterElement.textContent = target;
            }
        };
        requestAnimationFrame(animate);
    }
}

// ========================================
// Image Carousel
// ========================================
function initCarousel() {
    const track = document.querySelector('.gallery-track');
    const items = document.querySelectorAll('.gallery-item');
    const prevBtn = document.querySelector('.carousel-btn-prev');
    const nextBtn = document.querySelector('.carousel-btn-next');
    const dots = document.querySelectorAll('.dot');

    if (!track || items.length === 0) return;

    let currentIndex = 0;
    const totalItems = items.length;

    // Update carousel display
    function updateCarousel() {
        // Hide all items
        items.forEach(item => {
            item.classList.remove('active');
        });

        // Show current item
        items[currentIndex].classList.add('active');

        // Update dots
        dots.forEach((dot, index) => {
            if (index === currentIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }

    // Navigate to next slide
    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel();
    }

    // Navigate to previous slide
    function prevSlide() {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateCarousel();
    }

    // Navigate to specific slide
    function goToSlide(index) {
        currentIndex = index;
        updateCarousel();
    }

    // Event listeners
    if (nextBtn) {
        nextBtn.addEventListener('click', nextSlide);
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', prevSlide);
    }

    // Dot navigation
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => goToSlide(index));
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            prevSlide();
        } else if (e.key === 'ArrowRight') {
            nextSlide();
        }
    });

    // Auto-play (optional - commented out by default)
    // const autoPlayInterval = 5000; // 5 seconds
    // setInterval(nextSlide, autoPlayInterval);

    // Touch/swipe support for mobile
    let touchStartX = 0;
    let touchEndX = 0;

    track.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    track.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });

    function handleSwipe() {
        const swipeThreshold = 50; // Minimum distance for a swipe
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                // Swipe left - next slide
                nextSlide();
            } else {
                // Swipe right - previous slide
                prevSlide();
            }
        }
    }
}

// ========================================
// Smooth Scroll for Navigation Links
// ========================================
function initSmoothScroll() {
    const navLinks = document.querySelectorAll('a[href^="#"]');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const targetId = link.getAttribute('href');

            // Skip if it's just "#"
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                e.preventDefault();

                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ========================================
// Set Current Year in Footer
// ========================================
function setCurrentYear() {
    const yearElement = document.getElementById('current-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
}

// ========================================
// Header Scroll Effect (optional enhancement)
// ========================================
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (!header) return;

    if (window.scrollY > 50) {
        header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    } else {
        header.style.boxShadow = 'none';
    }
});

// ========================================
// Utility: Debounce Function
// ========================================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ========================================
// Window Resize Handler (debounced)
// ========================================
const handleResize = debounce(() => {
    // Add any resize-specific logic here if needed
    // Example: Recalculate carousel dimensions
}, 250);

window.addEventListener('resize', handleResize);

// ========================================
// Accessibility: Focus Visible Polyfill
// ========================================
document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        document.body.classList.add('user-is-tabbing');
    }
});

document.addEventListener('mousedown', () => {
    document.body.classList.remove('user-is-tabbing');
});
