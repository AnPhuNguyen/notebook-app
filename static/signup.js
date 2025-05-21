const form = document.getElementById('signupForm');
const messageDiv = document.getElementById('message');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    messageDiv.textContent = '';
    messageDiv.className = 'message';

    const username = form.name.value.trim();
    const email = form.email.value.trim();
    const password = form.password.value;

    // handle empty fields case in frontend
    if (!username) {
        messageDiv.textContent = 'Username is required.';
        messageDiv.classList.add('error');
        return;
    }
    if (!email) {
        messageDiv.textContent = 'Email is required.';
        messageDiv.classList.add('error');
        return;
    }
    if (!password) {
        messageDiv.textContent = 'Password is required.';
        messageDiv.classList.add('error');
        return;
    }

    const payload = { username, email, password };

    try {
        const response = await fetch('/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        if (response.ok) {
            const data = await response.json();
            messageDiv.textContent = data.message;
            messageDiv.classList.add('success');
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
