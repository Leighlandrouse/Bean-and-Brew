document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');

    registerForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        if (validateForm(username, email, password)) {
            // Simulate a registration process
            console.log('User registered:', { username, email, password });
            alert('Registration successful!');
            // Redirect to login page or another page
            window.location.href = 'login.html';
        }
    });

    function validateForm(username, email, password) {
        if (!username || !email || !password) {
            alert('All fields are required.');
            return false;
        }
        if (!validateEmail(email)) {
            alert('Please enter a valid email address.');
            return false;
        }
        if (password.length < 6) {
            alert('Password must be at least 6 characters long.');
            return false;
        }
        return true;
    }

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }
});