document.querySelector('.copy-btn').addEventListener('click', function() {
    const code = document.querySelector('code').innerText;
    navigator.clipboard.writeText(code).then(() => {
        this.innerText = 'Copied!';
        setTimeout(() => {
            this.innerText = 'Copy';
        }, 2000);
    });
});

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
