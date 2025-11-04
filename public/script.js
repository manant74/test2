// VibeTheForce - Main JavaScript
console.log('VibeTheForce initialized');

// Vote Manager - Handles API calls and vote persistence
const VoteManager = {
    USER_VOTED_KEY: 'vibetheforce_user_voted',
    SESSION_KEY: 'vibetheforce_session',

    // Submit vote to backend
    async submitVote(rating) {
        if (this.hasUserVoted()) {
            console.log('User has already voted');
            return false;
        }

        try {
            const response = await fetch('/.netlify/functions/vote', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    rating: parseInt(rating),
                    timestamp: new Date().toISOString(),
                    sessionId: this.getSessionId()
                })
            });

            if (response.ok) {
                localStorage.setItem(this.USER_VOTED_KEY, 'true');
                console.log('Vote submitted successfully');
                return true;
            } else {
                console.error('Failed to submit vote:', response.status);
                return false;
            }
        } catch (error) {
            console.error('Error submitting vote:', error);
            return false;
        }
    },

    // Get current vote counts from backend
    async getVoteCounts() {
        try {
            const response = await fetch('/.netlify/functions/results');
            if (response.ok) {
                return await response.json();
            } else {
                console.error('Failed to get results:', response.status);
                return null;
            }
        } catch (error) {
            console.error('Error getting results:', error);
            return null;
        }
    },

    // Check if user has already voted
    hasUserVoted() {
        return localStorage.getItem(this.USER_VOTED_KEY) === 'true';
    },

    // Get or create session ID
    getSessionId() {
        let sessionId = localStorage.getItem(this.SESSION_KEY);
        if (!sessionId) {
            sessionId = Date.now() + '-' + Math.random().toString(36).substring(2, 11);
            localStorage.setItem(this.SESSION_KEY, sessionId);
        }
        return sessionId;
    },

    // Reset vote status (for testing)
    resetVoteStatus() {
        localStorage.removeItem(this.USER_VOTED_KEY);
        console.log('Vote status reset');
    }
};

// Voting Interface - Handles UI interactions
const VotingInterface = {
    init() {
        this.attachEventListeners();
        this.attachNavigationListeners();
        this.checkVoteStatus();
    },

    // Attach click events to voting buttons
    attachEventListeners() {
        const voteButtons = document.querySelectorAll('.vote-button');
        voteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const rating = e.currentTarget.dataset.rating;
                this.handleVote(rating);
            });
        });
    },

    // Attach navigation event listeners
    attachNavigationListeners() {
        const viewResultsBtn = document.getElementById('view-results-btn');
        const viewResultsAlwaysBtn = document.getElementById('view-results-always-btn');
        const backToVoteBtn = document.getElementById('back-to-vote-btn');
        const retryBtn = document.getElementById('retry-btn');

        if (viewResultsBtn) {
            viewResultsBtn.addEventListener('click', () => {
                this.showResultsSection();
            });
        }

        if (viewResultsAlwaysBtn) {
            viewResultsAlwaysBtn.addEventListener('click', () => {
                this.showResultsSection();
            });
        }

        if (backToVoteBtn) {
            backToVoteBtn.addEventListener('click', () => {
                this.showVotingSection();
            });
        }

        if (retryBtn) {
            retryBtn.addEventListener('click', () => {
                this.hideErrorMessage();
            });
        }
    },

    // Show results section
    showResultsSection() {
        const votingSection = document.getElementById('voting-section');
        const resultsSection = document.getElementById('results-section');

        if (votingSection) votingSection.classList.add('hidden');
        if (resultsSection) {
            resultsSection.classList.remove('hidden');
            // Initialize results dashboard if not already done
            if (!ResultsDashboard.updateInterval) {
                ResultsDashboard.init();
            }
        }
    },

    // Show voting section
    showVotingSection() {
        const votingSection = document.getElementById('voting-section');
        const resultsSection = document.getElementById('results-section');

        // Clean up results dashboard when leaving
        if (ResultsDashboard.updateInterval) {
            ResultsDashboard.cleanup();
        }

        if (resultsSection) resultsSection.classList.add('hidden');
        if (votingSection) votingSection.classList.remove('hidden');
    },

    // Hide error message
    hideErrorMessage() {
        const errorMessage = document.getElementById('error-message');
        if (errorMessage) errorMessage.classList.add('hidden');
    },

    // Handle vote submission
    async handleVote(rating) {
        if (VoteManager.hasUserVoted()) {
            this.showMessage('Hai già votato! Grazie per il tuo feedback.', 'warning');
            return;
        }

        // Disable buttons during submission
        this.setButtonsEnabled(false);
        this.showLoadingOverlay(true);

        const success = await VoteManager.submitVote(rating);

        this.showLoadingOverlay(false);

        if (success) {
            this.showVoteConfirmation(rating);
            this.disableVotingInterface();
        } else {
            this.showMessage('Errore nell\'invio del voto. Riprova.', 'error');
            this.setButtonsEnabled(true);
        }
    },

    // Show visual confirmation after successful vote
    showVoteConfirmation(rating) {
        const ratingNames = {
            '1': 'Youngling',
            '2': 'Padawan',
            '3': 'Cavaliere Jedi',
            '4': 'Maestro Jedi',
            '5': 'Gran Maestro'
        };

        const button = document.querySelector(`[data-rating="${rating}"]`);
        if (button) {
            button.classList.add('vote-confirmed');

            // Add glow animation
            setTimeout(() => {
                button.classList.add('vote-glow');
            }, 100);
        }

        this.showMessage('success');

        // Show thank you message after a delay
        setTimeout(() => {
            this.showMessage('success');
        }, 2000);
    },

    // Disable voting interface after vote
    disableVotingInterface() {
        const voteButtons = document.querySelectorAll('.vote-button');
        voteButtons.forEach(button => {
            button.disabled = true;
            button.classList.add('disabled');
        });

        const votingSection = document.getElementById('voting-section');
        if (votingSection) {
            votingSection.classList.add('voting-complete');
        }
    },

    // Enable/disable voting buttons
    setButtonsEnabled(enabled) {
        const voteButtons = document.querySelectorAll('.vote-button');
        voteButtons.forEach(button => {
            button.disabled = !enabled;
            if (enabled) {
                button.classList.remove('disabled');
            } else {
                button.classList.add('disabled');
            }
        });
    },

    // Check if user has already voted and update UI accordingly
    checkVoteStatus() {
        if (VoteManager.hasUserVoted()) {
            this.disableVotingInterface();
            this.showMessage('info');
        }
    },

    // Show loading overlay
    showLoadingOverlay(show) {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            if (show) {
                loadingOverlay.classList.remove('hidden');
            } else {
                loadingOverlay.classList.add('hidden');
            }
        }
    },

    // Show message to user
    showMessage(type = 'info') {
        // Use existing HTML elements for messages
        const voteConfirmation = document.getElementById('vote-confirmation');
        const alreadyVoted = document.getElementById('already-voted');
        const errorMessage = document.getElementById('error-message');

        // Hide all message elements first
        [voteConfirmation, alreadyVoted, errorMessage].forEach(el => {
            if (el) el.classList.add('hidden');
        });

        if (type === 'success') {
            if (voteConfirmation) {
                voteConfirmation.classList.remove('hidden');
            }
        } else if (type === 'warning' || type === 'info') {
            if (alreadyVoted) {
                alreadyVoted.classList.remove('hidden');
            }
        } else if (type === 'error') {
            if (errorMessage) {
                errorMessage.classList.remove('hidden');
            }
        }
    }
};

// Results Dashboard - Handles real-time results display
const ResultsDashboard = {
    updateInterval: null,
    retryCount: 0,
    maxRetries: 3,
    isUpdating: false,

    init() {
        console.log('ResultsDashboard initialized');
        this.updateResults();
        this.startAutoUpdate();
    },

    // Update results display with error handling
    async updateResults() {
        // Prevent concurrent updates
        if (this.isUpdating) {
            return;
        }

        this.isUpdating = true;

        try {
            const results = await VoteManager.getVoteCounts();

            if (results) {
                this.renderResults(results);
                this.retryCount = 0; // Reset retry count on success
                this.hideConnectionError();
            } else {
                throw new Error('Failed to fetch results');
            }
        } catch (error) {
            console.error('Error updating results:', error);
            this.handleUpdateError();
        } finally {
            this.isUpdating = false;
        }
    },

    // Handle update errors with retry logic
    handleUpdateError() {
        this.retryCount++;

        if (this.retryCount >= this.maxRetries) {
            this.showConnectionError();
            console.warn(`Failed to update results after ${this.maxRetries} attempts`);
        } else {
            console.log(`Retry ${this.retryCount}/${this.maxRetries} for results update`);
        }
    },

    // Show connection error message
    showConnectionError() {
        const resultsContainer = document.querySelector('.results-container');
        if (resultsContainer) {
            let errorBanner = document.getElementById('connection-error-banner');

            if (!errorBanner) {
                errorBanner = document.createElement('div');
                errorBanner.id = 'connection-error-banner';
                errorBanner.className = 'connection-error-banner';
                errorBanner.innerHTML = `
                    <div class="error-banner-content">
                        <span class="error-banner-icon">⚠️</span>
                        <span class="error-banner-text">Connessione persa. Tentativo di riconnessione...</span>
                    </div>
                `;
                resultsContainer.insertBefore(errorBanner, resultsContainer.firstChild);
            }

            errorBanner.classList.remove('hidden');
        }
    },

    // Hide connection error message
    hideConnectionError() {
        const errorBanner = document.getElementById('connection-error-banner');
        if (errorBanner) {
            errorBanner.classList.add('hidden');
        }
    },

    // Render results in the dashboard with animations
    renderResults(results) {
        // Calculate statistics
        const totalVotes = Object.values(results).reduce((sum, count) => sum + count, 0);
        const average = totalVotes > 0 ?
            (Object.entries(results).reduce((sum, [rating, count]) => sum + (parseInt(rating) * count), 0) / totalVotes).toFixed(1) : '0.0';

        // Update stats with animation
        this.updateStatWithAnimation('total-votes', totalVotes);
        this.updateStatWithAnimation('average-rating', average);

        // Update chart bars for each rating level
        for (let rating = 1; rating <= 5; rating++) {
            const count = results[rating] || 0;
            const percentage = totalVotes > 0 ? Math.round((count / totalVotes) * 100) : 0;

            this.updateChartBar(rating, count, percentage);
        }

        // Add visual feedback for new votes
        this.highlightChanges();
    },

    // Update stat value with smooth animation
    updateStatWithAnimation(elementId, newValue) {
        const element = document.getElementById(elementId);
        if (!element) return;

        const currentValue = element.textContent;

        if (currentValue !== String(newValue)) {
            element.classList.add('stat-update');
            element.textContent = newValue;

            setTimeout(() => {
                element.classList.remove('stat-update');
            }, 500);
        }
    },

    // Update individual chart bar with smooth transition
    updateChartBar(rating, count, percentage) {
        const chartBar = document.querySelector(`.chart-bar[data-rating="${rating}"]`);
        const countEl = document.getElementById(`count-${rating}`);
        const percentageEl = document.getElementById(`percentage-${rating}`);

        if (chartBar) {
            // Smooth width transition
            chartBar.style.width = `${percentage}%`;

            // Add glow effect for non-zero values
            if (percentage > 0) {
                chartBar.classList.add('has-votes');
            } else {
                chartBar.classList.remove('has-votes');
            }
        }

        if (countEl) {
            const currentCount = parseInt(countEl.textContent) || 0;
            if (currentCount !== count) {
                countEl.classList.add('count-update');
                countEl.textContent = count;
                setTimeout(() => {
                    countEl.classList.remove('count-update');
                }, 500);
            }
        }

        if (percentageEl) {
            percentageEl.textContent = `${percentage}%`;
        }
    },

    // Highlight changes in the dashboard
    highlightChanges() {
        const resultsContainer = document.querySelector('.results-container');
        if (resultsContainer) {
            resultsContainer.classList.add('data-updated');
            setTimeout(() => {
                resultsContainer.classList.remove('data-updated');
            }, 300);
        }
    },

    // Start automatic updates every 2 seconds
    startAutoUpdate() {
        // Clear any existing interval
        this.stopAutoUpdate();

        console.log('Starting auto-update every 2 seconds');
        this.updateInterval = setInterval(() => {
            this.updateResults();
        }, 2000);
    },

    // Stop automatic updates
    stopAutoUpdate() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
            console.log('Auto-update stopped');
        }
    },

    // Clean up when leaving results view
    cleanup() {
        this.stopAutoUpdate();
        this.retryCount = 0;
        this.hideConnectionError();
    }
};

// QR Code Manager - Handles QR code generation and display
const QRCodeManager = {
    qrCodeUrl: null,
    appUrl: null,

    init() {
        this.appUrl = window.location.origin + window.location.pathname;
        this.generateQRCode();
        this.attachEventListeners();
    },

    // Generate QR code using qrserver.com API
    generateQRCode() {
        const size = 300;
        const encodedUrl = encodeURIComponent(this.appUrl);
        this.qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=${size}x${size}&data=${encodedUrl}`;

        // Set QR code image source
        const qrImage = document.getElementById('qr-code-image');
        if (qrImage) {
            qrImage.src = this.qrCodeUrl;
            qrImage.onerror = () => {
                console.error('Failed to load QR code image');
                this.showQRCodeError();
            };
        }

        // Set URL text
        const qrUrlText = document.getElementById('qr-url-text');
        if (qrUrlText) {
            qrUrlText.textContent = this.appUrl;
        }

        console.log('QR Code generated for:', this.appUrl);
    },

    // Show QR code error message
    showQRCodeError() {
        const qrWrapper = document.querySelector('.qr-code-wrapper');
        if (qrWrapper) {
            qrWrapper.innerHTML = `
                <div class="qr-error">
                    <p>⚠️ Impossibile caricare il QR Code</p>
                    <p class="qr-error-url">${this.appUrl}</p>
                </div>
            `;
        }
    },

    // Attach event listeners for QR code buttons
    attachEventListeners() {
        const floatingQrBtn = document.getElementById('floating-qr-btn');
        const toggleQrBtn = document.getElementById('toggle-qr-btn');
        const showQrFromResultsBtn = document.getElementById('show-qr-from-results-btn');

        if (floatingQrBtn) {
            floatingQrBtn.addEventListener('click', () => {
                this.toggleQRCodeSection();
            });
        }

        if (toggleQrBtn) {
            toggleQrBtn.addEventListener('click', () => {
                this.toggleQRCodeSection();
            });
        }

        if (showQrFromResultsBtn) {
            showQrFromResultsBtn.addEventListener('click', () => {
                this.showQRCodeSection();
            });
        }
    },

    // Toggle QR code section visibility
    toggleQRCodeSection() {
        const qrSection = document.getElementById('qr-code-section');
        const toggleBtn = document.getElementById('toggle-qr-btn');

        if (qrSection) {
            const isHidden = qrSection.classList.contains('hidden');

            if (isHidden) {
                qrSection.classList.remove('hidden');
                if (toggleBtn) toggleBtn.textContent = 'Nascondi QR Code';
            } else {
                qrSection.classList.add('hidden');
                if (toggleBtn) toggleBtn.textContent = 'Mostra QR Code';
            }
        }
    },

    // Show QR code section
    showQRCodeSection() {
        const qrSection = document.getElementById('qr-code-section');
        const toggleBtn = document.getElementById('toggle-qr-btn');

        if (qrSection) {
            qrSection.classList.remove('hidden');
            if (toggleBtn) toggleBtn.textContent = 'Nascondi QR Code';

            // Scroll to QR code section
            qrSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    },

    // Hide QR code section
    hideQRCodeSection() {
        const qrSection = document.getElementById('qr-code-section');
        const toggleBtn = document.getElementById('toggle-qr-btn');

        if (qrSection) {
            qrSection.classList.add('hidden');
            if (toggleBtn) toggleBtn.textContent = 'Mostra QR Code';
        }
    },

    // Get QR code URL for external use
    getQRCodeUrl() {
        return this.qrCodeUrl;
    },

    // Get app URL
    getAppUrl() {
        return this.appUrl;
    }
};

// Theme Engine - Handles Star Wars animations and effects
const ThemeEngine = {
    init() {
        this.applyStarWarsTheme();
        this.addAnimationEffects();
    },

    // Apply Star Wars theme classes
    applyStarWarsTheme() {
        document.body.classList.add('star-wars-theme');
    },

    // Add hover and interaction effects
    addAnimationEffects() {
        const voteButtons = document.querySelectorAll('.vote-button');
        voteButtons.forEach(button => {
            button.addEventListener('mouseenter', () => {
                button.classList.add('hover-glow');
            });

            button.addEventListener('mouseleave', () => {
                button.classList.remove('hover-glow');
            });
        });
    },

    // Animate vote button when clicked
    animateVote(rating) {
        const button = document.querySelector(`[data-rating="${rating}"]`);
        if (button) {
            button.classList.add('vote-animation');
            setTimeout(() => {
                button.classList.remove('vote-animation');
            }, 1000);
        }
    }
};

// Application Initialization
document.addEventListener('DOMContentLoaded', () => {
    console.log('VibeTheForce DOM loaded, initializing...');

    // Initialize all components
    ThemeEngine.init();
    VotingInterface.init();
    QRCodeManager.init();

    // Initialize results dashboard if results section exists
    if (document.getElementById('results-section')) {
        // Don't auto-initialize results dashboard, let navigation handle it
        console.log('Results section found, will initialize on demand');
    }

    console.log('VibeTheForce fully initialized');
});

// Expose utilities for debugging (development only)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.VibeTheForce = {
        VoteManager,
        VotingInterface,
        ResultsDashboard,
        ThemeEngine,
        QRCodeManager
    };
}