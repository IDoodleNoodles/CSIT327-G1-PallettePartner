/**
 * Sweet Artistic Alert System for PallettePartner
 * 
 * USAGE EXAMPLES:
 * 
 * 1. Basic usage:
 *    sweetAlert.success('Artwork uploaded successfully!');
 *    sweetAlert.error('Failed to save changes.');
 *    sweetAlert.warning('Session will expire soon.');
 *    sweetAlert.info('New feature available!');
 * 
 * 2. Custom duration:
 *    sweetAlert.show('Custom message', 'success', 5000); // 5 seconds
 * 
 * 3. From Django views:
 *    messages.success(request, 'Profile updated!')
 *    messages.error(request, 'Invalid credentials')
 *    messages.warning(request, 'Please verify your email')
 *    messages.info(request, 'Welcome to PallettePartner')
 * 
 * 4. Manual removal:
 *    const alert = sweetAlert.success('Processing...');
 *    setTimeout(() => sweetAlert.remove(alert), 2000);
 */

class SweetAlert {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {
        // Create container for alerts if it doesn't exist
        if (!document.getElementById('sweet-alert-container')) {
            this.container = document.createElement('div');
            this.container.id = 'sweet-alert-container';
            this.container.className = 'fixed top-6 right-6 z-[9999] flex flex-col gap-3 pointer-events-none';
            document.body.appendChild(this.container);
        } else {
            this.container = document.getElementById('sweet-alert-container');
        }
    }

    /**
     * Show alert with type and message
     * @param {string} message - The message to display
     * @param {string} type - success, error, warning, info
     * @param {number} duration - Duration in milliseconds (default: 4000)
     */
    show(message, type = 'info', duration = 4000) {
        const alert = this.createAlert(message, type);
        this.container.appendChild(alert);

        // Trigger animation
        setTimeout(() => {
            alert.style.opacity = '1';
            alert.style.transform = 'translateX(0) scale(1)';
        }, 10);

        // Auto remove after duration
        setTimeout(() => {
            this.remove(alert);
        }, duration);

        return alert;
    }

    createAlert(message, type) {
        const alert = document.createElement('div');
        alert.className = 'sweet-alert pointer-events-auto';
        
        const config = this.getTypeConfig(type);
        
        alert.innerHTML = `
            <div class="relative overflow-hidden rounded-2xl shadow-2xl backdrop-blur-md border-2 ${config.borderColor} bg-gradient-to-br ${config.gradient} p-4 min-w-[320px] max-w-md">
                <!-- Animated Background Pattern -->
                <div class="absolute inset-0 opacity-10">
                    <div class="floating-pattern pattern-1"></div>
                    <div class="floating-pattern pattern-2"></div>
                    <div class="floating-pattern pattern-3"></div>
                </div>
                
                <!-- Content -->
                <div class="relative flex items-start gap-4">
                    <!-- Icon -->
                    <div class="flex-shrink-0">
                        <div class="w-12 h-12 rounded-full ${config.iconBg} flex items-center justify-center animate-bounce-subtle">
                            ${config.icon}
                        </div>
                    </div>
                    
                    <!-- Message -->
                    <div class="flex-1 pt-1">
                        <p class="text-white font-semibold text-sm leading-relaxed">
                            ${message}
                        </p>
                    </div>
                    
                    <!-- Close Button -->
                    <button onclick="sweetAlert.remove(this.closest('.sweet-alert'))" 
                            class="flex-shrink-0 w-8 h-8 rounded-full ${config.closeBg} flex items-center justify-center hover:scale-110 transition-transform duration-200">
                        <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
                
                <!-- Progress Bar -->
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-white/20 overflow-hidden">
                    <div class="h-full ${config.progressBg} animate-progress"></div>
                </div>
            </div>
        `;

        // Style
        alert.style.opacity = '0';
        alert.style.transform = 'translateX(100px) scale(0.9)';
        alert.style.transition = 'all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)';

        return alert;
    }

    getTypeConfig(type) {
        const configs = {
            success: {
                gradient: 'from-emerald-500/90 to-teal-600/90',
                borderColor: 'border-emerald-400/50',
                iconBg: 'bg-white/20',
                closeBg: 'bg-white/10 hover:bg-white/20',
                progressBg: 'bg-emerald-300',
                icon: `<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>`
            },
            error: {
                gradient: 'from-red-500/90 to-rose-600/90',
                borderColor: 'border-red-400/50',
                iconBg: 'bg-white/20',
                closeBg: 'bg-white/10 hover:bg-white/20',
                progressBg: 'bg-red-300',
                icon: `<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>`
            },
            warning: {
                gradient: 'from-amber-500/90 to-orange-600/90',
                borderColor: 'border-amber-400/50',
                iconBg: 'bg-white/20',
                closeBg: 'bg-white/10 hover:bg-white/20',
                progressBg: 'bg-amber-300',
                icon: `<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>`
            },
            info: {
                gradient: 'from-blue-500/90 to-indigo-600/90',
                borderColor: 'border-blue-400/50',
                iconBg: 'bg-white/20',
                closeBg: 'bg-white/10 hover:bg-white/20',
                progressBg: 'bg-blue-300',
                icon: `<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>`
            }
        };

        return configs[type] || configs.info;
    }

    remove(alert) {
        if (!alert) return;
        
        alert.style.opacity = '0';
        alert.style.transform = 'translateX(100px) scale(0.9)';
        
        setTimeout(() => {
            if (alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
        }, 400);
    }

    // Helper methods for common use cases
    success(message, duration = 4000) {
        return this.show(message, 'success', duration);
    }

    error(message, duration = 5000) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration = 4500) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration = 4000) {
        return this.show(message, 'info', duration);
    }
}

// Initialize global instance
const sweetAlert = new SweetAlert();

// Make it available globally
window.sweetAlert = sweetAlert;

// Auto-show Django messages on page load
document.addEventListener('DOMContentLoaded', () => {
    const djangoMessages = document.querySelectorAll('.django-message');
    djangoMessages.forEach((msg) => {
        const type = msg.dataset.type || 'info';
        const text = msg.textContent.trim();
        sweetAlert.show(text, type);
        msg.remove(); // Remove the hidden element
    });
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes bounce-subtle {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-4px);
        }
    }

    @keyframes progress {
        from {
            transform: translateX(-100%);
        }
        to {
            transform: translateX(0);
        }
    }

    @keyframes float-pattern {
        0%, 100% {
            transform: translate(0, 0) rotate(0deg);
        }
        25% {
            transform: translate(10px, -10px) rotate(5deg);
        }
        50% {
            transform: translate(-5px, -15px) rotate(-3deg);
        }
        75% {
            transform: translate(-10px, -5px) rotate(4deg);
        }
    }

    .animate-bounce-subtle {
        animation: bounce-subtle 2s ease-in-out infinite;
    }

    .animate-progress {
        animation: progress 4s linear forwards;
    }

    .floating-pattern {
        position: absolute;
        background: white;
        border-radius: 50%;
        opacity: 0.3;
        animation: float-pattern 15s ease-in-out infinite;
    }

    .pattern-1 {
        width: 60px;
        height: 60px;
        top: 10%;
        left: 10%;
        animation-delay: 0s;
    }

    .pattern-2 {
        width: 40px;
        height: 40px;
        top: 60%;
        right: 15%;
        animation-delay: 2s;
    }

    .pattern-3 {
        width: 50px;
        height: 50px;
        bottom: 20%;
        left: 60%;
        animation-delay: 4s;
    }

    /* Smooth scrollbar for alerts container */
    #sweet-alert-container {
        max-height: calc(100vh - 3rem);
        overflow-y: auto;
        scrollbar-width: none;
    }

    #sweet-alert-container::-webkit-scrollbar {
        display: none;
    }
`;
document.head.appendChild(style);
