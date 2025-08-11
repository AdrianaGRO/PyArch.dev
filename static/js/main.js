// Enhanced Blog Manager with Theme Toggle and Scroll Effects
class BlogManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        this.setupTheme();
        this.setupScrollEffects();
        this.setupImageUpload();
        this.setupFormHandling();
        this.setupAnimations();
    }

    setupTheme() {
        document.body.setAttribute('data-theme', this.currentTheme);
        
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
                document.body.setAttribute('data-theme', this.currentTheme);
                localStorage.setItem('theme', this.currentTheme);
            });
        }
    }

    setupScrollEffects() {
        const header = document.getElementById('header');
        const scrollProgress = document.getElementById('scrollProgress');

        if (scrollProgress) {
            window.addEventListener('scroll', () => {
                const scrollTop = window.pageYOffset;
                const docHeight = document.documentElement.scrollHeight - window.innerHeight;
                const scrollPercent = (scrollTop / docHeight) * 100;

                // Update progress bar
                scrollProgress.style.width = scrollPercent + '%';

                // Header scroll effect
                if (header && scrollTop > 100) {
                    header.classList.add('scrolled');
                } else if (header) {
                    header.classList.remove('scrolled');
                }
            });
        }
    }

    setupImageUpload() {
        const imageUpload = document.getElementById('image-upload');
        const imagePreview = document.getElementById('image-preview');
        
        if (imageUpload && imagePreview) {
            imageUpload.addEventListener('change', function() {
                // Clear the preview
                imagePreview.innerHTML = '';
                
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.alt = 'Preview';
                        
                        // Add a remove button
                        const removeBtn = document.createElement('button');
                        removeBtn.type = 'button';
                        removeBtn.className = 'remove-image-btn';
                        removeBtn.textContent = 'Remove';
                        removeBtn.addEventListener('click', function() {
                            imagePreview.innerHTML = '';
                            imageUpload.value = '';
                        });
                        
                        // Add both to the preview
                        imagePreview.appendChild(img);
                        imagePreview.appendChild(removeBtn);
                    };
                    
                    reader.readAsDataURL(this.files[0]);
                }
            });
        }
    }

    setupFormHandling() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                // We'll keep the default form submission but add a loading state to the button
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    const originalText = submitBtn.textContent;
                    submitBtn.innerHTML = '<div class="loading"></div> Submitting...';
                    // The form will still submit and process as normal
                }
            });
        });
    }

    setupAnimations() {
        // Intersection Observer for animations
        if ('IntersectionObserver' in window) {
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }
                });
            }, observerOptions);

            // Observe cards and posts for stagger animation
            const animatedElements = document.querySelectorAll('.card, .post');
            animatedElements.forEach((element, index) => {
                element.style.opacity = '0';
                element.style.transform = 'translateY(20px)';
                element.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
                observer.observe(element);
            });
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize blog manager
    new BlogManager();
});

// Performance optimization: Debounced scroll handler
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
