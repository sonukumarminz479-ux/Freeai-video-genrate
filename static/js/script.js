// General utilities
function toggleAdvanced() {
    const settings = document.getElementById('advancedSettings');
    if (settings) {
        settings.style.display = settings.style.display === 'none' ? 'block' : 'none';
    }
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 8;
}

// Close modals
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('close-modal') || e.target.classList.contains('modal')) {
        e.target.closest('.modal').style.display = 'none';
    }
});

// Close dropdown when clicking outside
document.addEventListener('click', function(e) {
    if (!e.target.closest('.user-menu')) {
        document.querySelectorAll('.dropdown').forEach(d => d.style.display = 'none');
    }
});
