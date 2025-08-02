/**
 * MutaSight AI - Main JavaScript utilities and functionality
 * Drug Discovery Platform - Core JavaScript functions
 */

// Global utilities and helper functions
const MutaSightApp = {
    // Application configuration
    config: {
        apiEndpoint: '/api',
        socketEndpoint: '/',
        chartColors: ['#2c5aa0', '#27ae60', '#3498db', '#f39c12', '#e74c3c', '#9b59b6'],
        animationDuration: 300
    },

    // Initialize the application
    init: function() {
        this.setupGlobalEventListeners();
        this.initializeTooltips();
        this.initializeModals();
        this.setupFormValidation();
        this.initializeCharts();
        this.setupSearchFunctionality();
        console.log('MutaSight AI platform initialized');
    },

    // Set up global event listeners
    setupGlobalEventListeners: function() {
        // Handle navigation active states
        this.updateActiveNavigation();
        
        // Handle form submissions with loading states
        document.addEventListener('submit', this.handleFormSubmission);
        
        // Handle AJAX errors globally
        window.addEventListener('unhandledrejection', this.handleGlobalErrors);
        
        // Handle page visibility changes
        document.addEventListener('visibilitychange', this.handleVisibilityChange);
        
        // Handle browser back/forward navigation
        window.addEventListener('popstate', this.handlePopState);
    },

    // Update active navigation based on current page
    updateActiveNavigation: function() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && currentPath.includes(href) && href !== '/') {
                link.classList.add('active');
            } else if (href === '/' && currentPath === '/') {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    },

    // Initialize Bootstrap tooltips
    initializeTooltips: function() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    },

    // Initialize Bootstrap modals
    initializeModals: function() {
        const modalElements = document.querySelectorAll('.modal');
        modalElements.forEach(modalEl => {
            modalEl.addEventListener('shown.bs.modal', function() {
                const firstInput = this.querySelector('input, textarea, select');
                if (firstInput) {
                    firstInput.focus();
                }
            });
        });
    },

    // Set up form validation
    setupFormValidation: function() {
        const forms = document.querySelectorAll('.needs-validation');
        forms.forEach(form => {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    },

    // Handle form submissions with loading states
    handleFormSubmission: function(event) {
        const form = event.target;
        const submitButton = form.querySelector('button[type="submit"]');
        
        if (submitButton && !form.classList.contains('no-loading')) {
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            submitButton.disabled = true;
            
            // Re-enable button after 10 seconds as fallback
            setTimeout(() => {
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }, 10000);
        }
    },

    // Initialize charts
    initializeCharts: function() {
        // Set default Chart.js configuration
        if (typeof Chart !== 'undefined') {
            Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
            Chart.defaults.color = '#666';
            Chart.defaults.plugins.legend.labels.usePointStyle = true;
        }
    },

    // Set up search functionality
    setupSearchFunctionality: function() {
        const searchInputs = document.querySelectorAll('input[type="search"], .search-input');
        
        searchInputs.forEach(input => {
            let searchTimeout;
            input.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    MutaSightApp.performSearch(this);
                }, 300);
            });
        });
    },

    // Perform search functionality
    performSearch: function(input) {
        const searchTerm = input.value.toLowerCase().trim();
        const targetSelector = input.getAttribute('data-search-target');
        
        if (targetSelector) {
            const targets = document.querySelectorAll(targetSelector);
            targets.forEach(target => {
                const searchText = target.textContent.toLowerCase();
                const isVisible = searchText.includes(searchTerm);
                target.style.display = isVisible ? '' : 'none';
            });
            
            // Show "no results" message if needed
            this.showSearchResults(targets, searchTerm);
        }
    },

    // Show search results message
    showSearchResults: function(targets, searchTerm) {
        const visibleTargets = Array.from(targets).filter(t => t.style.display !== 'none');
        const container = targets[0]?.parentElement;
        
        if (container) {
            let noResultsMsg = container.querySelector('.no-search-results');
            
            if (visibleTargets.length === 0 && searchTerm) {
                if (!noResultsMsg) {
                    noResultsMsg = document.createElement('div');
                    noResultsMsg.className = 'no-search-results text-center text-muted py-4';
                    noResultsMsg.innerHTML = `
                        <i class="fas fa-search fa-2x mb-3"></i>
                        <p>No results found for "${searchTerm}"</p>
                    `;
                    container.appendChild(noResultsMsg);
                }
                noResultsMsg.style.display = 'block';
            } else if (noResultsMsg) {
                noResultsMsg.style.display = 'none';
            }
        }
    },

    // Handle global errors
    handleGlobalErrors: function(event) {
        console.error('Unhandled promise rejection:', event.reason);
        MutaSightApp.showNotification('An unexpected error occurred. Please try again.', 'danger');
    },

    // Handle page visibility changes
    handleVisibilityChange: function() {
        if (document.hidden) {
            // Page is hidden - pause any ongoing animations/timers
            MutaSightApp.pauseAnimations();
        } else {
            // Page is visible - resume animations/timers
            MutaSightApp.resumeAnimations();
        }
    },

    // Handle browser navigation
    handlePopState: function(event) {
        MutaSightApp.updateActiveNavigation();
    },

    // Pause animations when page is hidden
    pauseAnimations: function() {
        const animatedElements = document.querySelectorAll('.animated, .fade-in-up');
        animatedElements.forEach(el => {
            el.style.animationPlayState = 'paused';
        });
    },

    // Resume animations when page is visible
    resumeAnimations: function() {
        const animatedElements = document.querySelectorAll('.animated, .fade-in-up');
        animatedElements.forEach(el => {
            el.style.animationPlayState = 'running';
        });
    },

    // Show notification
    showNotification: function(message, type = 'info', duration = 4000) {
        const notification = document.createElement('div');
        notification.className = 'position-fixed top-0 end-0 m-3 notification-toast';
        notification.style.zIndex = '9999';
        
        const alertClass = type === 'error' ? 'danger' : type;
        notification.innerHTML = `
            <div class="alert alert-${alertClass} alert-dismissible fade show" role="alert">
                <i class="fas fa-${this.getNotificationIcon(type)} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        document.body.appendChild(notification);

        // Auto-remove after specified duration
        setTimeout(() => {
            if (notification.parentNode) {
                const alert = notification.querySelector('.alert');
                if (alert) {
                    const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                    bsAlert.close();
                }
            }
        }, duration);

        return notification;
    },

    // Get notification icon based on type
    getNotificationIcon: function(type) {
        const icons = {
            'success': 'check-circle',
            'info': 'info-circle',
            'warning': 'exclamation-triangle',
            'danger': 'exclamation-circle',
            'error': 'exclamation-circle'
        };
        return icons[type] || 'info-circle';
    },

    // Confirm dialog
    confirmDialog: function(message, title = 'Confirm Action') {
        return new Promise((resolve) => {
            const modal = document.createElement('div');
            modal.className = 'modal fade';
            modal.innerHTML = `
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>${message}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-danger confirm-btn">Confirm</button>
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);
            const bsModal = new bootstrap.Modal(modal);
            
            modal.addEventListener('click', function(e) {
                if (e.target.classList.contains('confirm-btn')) {
                    resolve(true);
                    bsModal.hide();
                } else if (e.target.hasAttribute('data-bs-dismiss')) {
                    resolve(false);
                }
            });

            modal.addEventListener('hidden.bs.modal', function() {
                document.body.removeChild(modal);
            });

            bsModal.show();
        });
    },

    // Format numbers for display
    formatNumber: function(num, decimals = 2) {
        if (num === null || num === undefined) return 'N/A';
        return parseFloat(num).toFixed(decimals);
    },

    // Format dates for display
    formatDate: function(date, format = 'short') {
        if (!date) return 'N/A';
        
        const d = typeof date === 'string' ? new Date(date) : date;
        
        if (format === 'short') {
            return d.toLocaleDateString();
        } else if (format === 'long') {
            return d.toLocaleDateString(undefined, { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
        } else if (format === 'datetime') {
            return d.toLocaleString();
        }
        
        return d.toLocaleDateString();
    },

    // Debounce function
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },

    // Copy text to clipboard
    copyToClipboard: function(text) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Copied to clipboard', 'success', 2000);
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'absolute';
            textArea.style.left = '-999999px';
            document.body.prepend(textArea);
            textArea.select();
            
            try {
                document.execCommand('copy');
                this.showNotification('Copied to clipboard', 'success', 2000);
            } catch (error) {
                this.showNotification('Failed to copy to clipboard', 'danger');
            } finally {
                textArea.remove();
            }
        }
    },

    // Download file from blob
    downloadBlob: function(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    },

    // Create loading overlay
    showLoadingOverlay: function(target = document.body, message = 'Loading...') {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay position-absolute w-100 h-100 d-flex align-items-center justify-content-center';
        overlay.style.cssText = 'top: 0; left: 0; background: rgba(255,255,255,0.9); z-index: 1000;';
        overlay.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary mb-3" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="text-muted">${message}</p>
            </div>
        `;
        
        target.style.position = 'relative';
        target.appendChild(overlay);
        return overlay;
    },

    // Remove loading overlay
    hideLoadingOverlay: function(target = document.body) {
        const overlay = target.querySelector('.loading-overlay');
        if (overlay) {
            overlay.remove();
        }
    },

    // Animate counter
    animateCounter: function(element, start, end, duration = 1000) {
        const startTime = performance.now();
        const difference = end - start;
        
        const step = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const current = start + (difference * this.easeOutQuart(progress));
            
            element.textContent = Math.floor(current);
            
            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                element.textContent = end;
            }
        };
        
        requestAnimationFrame(step);
    },

    // Easing function for animations
    easeOutQuart: function(t) {
        return 1 - Math.pow(1 - t, 4);
    },

    // Validate email format
    validateEmail: function(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    // Validate SMILES notation (basic)
    validateSMILES: function(smiles) {
        if (!smiles || typeof smiles !== 'string') return false;
        
        // Check for balanced brackets
        let roundBrackets = 0;
        let squareBrackets = 0;
        
        for (let char of smiles) {
            if (char === '(') roundBrackets++;
            else if (char === ')') roundBrackets--;
            else if (char === '[') squareBrackets++;
            else if (char === ']') squareBrackets--;
            
            if (roundBrackets < 0 || squareBrackets < 0) return false;
        }
        
        return roundBrackets === 0 && squareBrackets === 0;
    },

    // Generate random ID
    generateId: function(prefix = 'id') {
        return prefix + '_' + Math.random().toString(36).substr(2, 9);
    },

    // Check if element is in viewport
    isInViewport: function(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    },

    // Scroll to element smoothly
    scrollToElement: function(element, offset = 0) {
        const elementPosition = element.offsetTop - offset;
        window.scrollTo({
            top: elementPosition,
            behavior: 'smooth'
        });
    }
};

// Scientific calculation utilities
const ScientificUtils = {
    // Calculate molecular weight from formula
    calculateMolecularWeight: function(formula) {
        const atomicWeights = {
            'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.811,
            'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
            'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974,
            'S': 32.065, 'Cl': 35.453, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
            'Sc': 44.956, 'Ti': 47.867, 'V': 50.942, 'Cr': 51.996, 'Mn': 54.938,
            'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.409,
            'Ga': 69.723, 'Ge': 72.641, 'As': 74.922, 'Se': 78.963, 'Br': 79.904,
            'Kr': 83.798, 'Rb': 85.468, 'Sr': 87.62, 'Y': 88.906, 'Zr': 91.224,
            'Nb': 92.906, 'Mo': 95.96, 'Tc': 98, 'Ru': 101.07, 'Rh': 102.906,
            'Pd': 106.42, 'Ag': 107.868, 'Cd': 112.411, 'In': 114.818, 'Sn': 118.710,
            'Sb': 121.760, 'Te': 127.6, 'I': 126.904, 'Xe': 131.293
        };

        let weight = 0;
        const matches = formula.match(/([A-Z][a-z]?)(\d*)/g);
        
        if (matches) {
            matches.forEach(match => {
                const element = match.match(/[A-Z][a-z]?/)[0];
                const count = match.match(/\d+/);
                const num = count ? parseInt(count[0]) : 1;
                
                if (atomicWeights[element]) {
                    weight += atomicWeights[element] * num;
                }
            });
        }

        return Math.round(weight * 100) / 100;
    },

    // Convert temperature units
    convertTemperature: function(value, fromUnit, toUnit) {
        // Convert to Celsius first
        let celsius;
        switch (fromUnit.toLowerCase()) {
            case 'f':
            case 'fahrenheit':
                celsius = (value - 32) * 5/9;
                break;
            case 'k':
            case 'kelvin':
                celsius = value - 273.15;
                break;
            case 'c':
            case 'celsius':
            default:
                celsius = value;
                break;
        }

        // Convert from Celsius to target unit
        switch (toUnit.toLowerCase()) {
            case 'f':
            case 'fahrenheit':
                return celsius * 9/5 + 32;
            case 'k':
            case 'kelvin':
                return celsius + 273.15;
            case 'c':
            case 'celsius':
            default:
                return celsius;
        }
    },

    // Convert concentration units
    convertConcentration: function(value, fromUnit, toUnit, molecularWeight = null) {
        // This is a simplified conversion - real implementation would be more complex
        const conversions = {
            'mg/ml_to_mm': (val, mw) => mw ? (val / mw) * 1000 : null,
            'mm_to_mg/ml': (val, mw) => mw ? (val * mw) / 1000 : null,
            'g/l_to_mg/ml': (val) => val,
            'mg/ml_to_g/l': (val) => val
        };

        const conversionKey = `${fromUnit}_to_${toUnit}`;
        const converter = conversions[conversionKey];
        
        return converter ? converter(value, molecularWeight) : value;
    }
};

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    MutaSightApp.init();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MutaSightApp, ScientificUtils };
}
