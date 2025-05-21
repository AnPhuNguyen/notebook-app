const form = document.getElementById('loginForm');
const messageDiv = document.getElementById('message');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    messageDiv.textContent = '';
    messageDiv.className = 'message';

    const info = form.info.value.trim();
    const password = form.password.value;

    // handle empty input case in frontend
    if (!info) {
        messageDiv.textContent = 'Username or Email is required.';
        messageDiv.classList.add('error');
        return;
    }
    if (!password) {
        messageDiv.textContent = 'Password is required.';
        messageDiv.classList.add('error');
        return;
    }

    const payload = { info, password };

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        if (response.ok) {
            const data = await response.json();
            messageDiv.textContent = data.message;
            messageDiv.classList.add('success');
            // Redirect to notebook interface after successful login
            window.location.href = "/user/me/main";
        } else {
            const errorData = await response.json();
            messageDiv.textContent = 'Error: ' + errorData.detail;
            messageDiv.classList.add('error');
        }
    } catch (error) {
        messageDiv.textContent = 'Network error: ' + error.message;
        messageDiv.classList.add('error');
    }
});
