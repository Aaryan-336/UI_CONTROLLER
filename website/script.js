// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Setup Box Hover Effect
const setupBox = document.querySelector('.setup-box');
if (setupBox) {
    setupBox.addEventListener('click', () => {
        const code = document.getElementById('cli').innerText;
        navigator.clipboard.writeText(code);
        alert('Terminal command copied to clipboard!');
    });
}
