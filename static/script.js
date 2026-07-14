// Wait for the entire webpage to load before running any script
document.addEventListener("DOMContentLoaded", () => {
    // --- SELECTING UI ELEMENTS ---
    const searchBar = document.querySelector('.search-bar-container');
    const loginBtn = document.querySelector('#login-btn');
    const loginPopup = document.querySelector('.login-form-container');
    const formClose = document.querySelector('#form-close');
    const menu = document.querySelector('#menu-bar');
    const navbar = document.querySelector('.navbar');
    const videoBtns = document.querySelectorAll('.vid-btn');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const registerLink = document.getElementById('register-link');
    const loginLink = document.getElementById('login-link');

    // --- UI INTERACTIVITY ---
    // Show login/register popup
    loginBtn?.addEventListener('click', () => {
        loginPopup.classList.add('active');
    });
    // Hide login/register popup
    formClose?.addEventListener('click', () => {
        loginPopup.classList.remove('active');
    });
    // Toggle mobile navigation menu
    menu?.addEventListener('click', () => {
        menu.classList.toggle('fa-times');
        navbar.classList.toggle('active');
    });
    // Close popups and menus on scroll
    window.onscroll = () => {
        searchBtn?.classList.remove('fa-times');
        searchBar?.classList.remove('active');
        menu?.classList.remove('fa-times');
        navbar?.classList.remove('active');
        loginPopup?.classList.remove('active');
    };
    // Switch between login and registration forms inside the popup
    registerLink?.addEventListener('click', (e) => {
        e.preventDefault();
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    });
    loginLink?.addEventListener('click', (e) => {
        e.preventDefault();
        registerForm.style.display = 'none';
        loginForm.style.display = 'block';
    });


    // Home page video slider controls
    videoBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelector('.controls .active')?.classList.remove('active');
            btn.classList.add('active');
            const src = btn.getAttribute('data-src');
            const videoSlider = document.querySelector('#video-slider');
            if (videoSlider) {
                videoSlider.src = src;
            }
        });
    });

    // --- API COMMUNICATION (LOGIN & REGISTER) ---
    // Handle user registration
    registerForm?.addEventListener('submit', (e) => {
        e.preventDefault(); 

        const name = registerForm.querySelector('input[name="name"]').value;
        const email = registerForm.querySelector('input[name="email"]').value;
        const password = registerForm.querySelector('input[name="password"]').value;

        const userData = {
            name: name,
            email: email,
            password: password
        };
        fetch('/api/register', { // Using relative path is better
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
            })
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(res => {
                alert(res.body.message);
                
                // ✅ CHANGED: On successful registration, redirect to the homepage
                if (res.status === 201) { // 201 Created is the success status for new resource
                    window.location.href = '/';
                }
            })
            .catch(error => {
                console.error('Registration Error:', error);
                alert('An error occurred. Please try again.');
            });
    });

    // Handle user login
    loginForm?.addEventListener('submit', (e) => {
        e.preventDefault(); 
        const email = loginForm.querySelector('input[name="email"]').value;
        const password = loginForm.querySelector('input[name="password"]').value;
        const loginData = {
            email: email,
            password: password
        };
        fetch('/api/login', { // Using relative path is better
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loginData),
            })
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(res => {
                alert(res.body.message); // Show message from server
                
                // ✅ CHANGED: Check for successful status and redirect to homepage
                if (res.status === 200) {
                    window.location.href = '/';
                }
            })
            .catch(error => {
                console.error('Login Error:', error);
                alert('Login failed. Please check your credentials or server connection.');
            });
    });
});