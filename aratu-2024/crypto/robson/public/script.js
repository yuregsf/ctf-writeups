document.addEventListener('DOMContentLoaded', () => {
    const generateRandomBtn = document.getElementById('generate-random');
    const randomResult = document.getElementById('random-result');
    const updateTokenBtn = document.getElementById('update-token-btn');
    const updateTokenResult = document.getElementById('update-token-result');
    const adminLoginBtn = document.getElementById('admin-login-btn');
    const adminContent = document.getElementById('admin-content');
    const adminMessage = document.getElementById('admin-message');
    const fetchFlagBtn = document.getElementById('fetch-flag-btn');
    const flagContent = document.getElementById('flag-content');

    let currentUsername = '';
    let currentToken = '';

    if (generateRandomBtn) {
        generateRandomBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/api/random');
                const data = await response.json();
                randomResult.textContent = `${data.numbers.join(', ')}`;
            } catch (error) {
                randomResult.textContent = 'Error generating random numbers';
            }
        });
    }

    if (updateTokenBtn) {
        updateTokenBtn.addEventListener('click', async () => {
            const username = document.getElementById('username').value;
            try {
                const response = await fetch('/api/update-token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username }),
                });
                const data = await response.json();
                updateTokenResult.textContent = data.message;
            } catch (error) {
                updateTokenResult.textContent = 'Error updating token';
            }
        });
    }

    if (adminLoginBtn) {
        adminLoginBtn.addEventListener('click', async () => {
            const username = document.getElementById('admin-username').value;
            const token = document.getElementById('admin-token').value;
            try {
                const response = await fetch('/api/admin', {
                    headers: {
                        'x-api-token': token,
                        'x-username': username,
                    },
                });
                const data =     await response.json();
                if (response.ok) {
                    adminContent.style.display = 'block';
                    adminMessage.textContent = data.message;
                    currentUsername = username;
                    currentToken = token;
                } else {
                    adminMessage.textContent = 'Authentication failed';
                }
            } catch (error) {
                adminMessage.textContent = 'Error accessing admin panel';
            }
        });
    }

    if (fetchFlagBtn) {
        fetchFlagBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/api/flag', {
                    headers: {
                        'x-api-token': currentToken,
                        'x-username': currentUsername,
                    },
                });
                const data = await response.json();
                if (response.ok) {
                    flagContent.textContent = `Flag: ${data.flag}`;
                } else {
                    flagContent.textContent = 'Error fetching flag';
                }
            } catch (error) {
                flagContent.textContent = 'Error fetching flag';
            }
        });
    }
});