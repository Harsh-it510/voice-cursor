// You can add JavaScript functionality here if needed.
// For a basic static portfolio, JavaScript might not be strictly necessary
// beyond simple interactions like smooth scrolling or form validation.

// Example: Smooth scrolling for navigation links
document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
