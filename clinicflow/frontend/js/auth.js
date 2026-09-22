document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    
    // Simple router
    const path = window.location.pathname;
    
    if (!token && path !== '/login.html' && path !== '/') {
        window.location.href = '/login.html';
        return;
    }

    if (token && (path === '/login.html' || path === '/')) {
        window.location.href = '/dashboard.html';
        return;
    }

    // Set user info in UI if logged in
    if (token) {
        setupUserInterface();
    }
});

async function setupUserInterface() {
    try {
        const user = await window.api.getMe();
        
        // Update user name in topbar
        const userNameEl = document.getElementById('user-name');
        if (userNameEl) userNameEl.textContent = user.nome;

        // Apply role-based visibility
        const userRole = user.role.toLowerCase();
        document.body.setAttribute('data-role', userRole);
        
        if (userRole !== 'admin') {
            document.querySelectorAll('.admin-only').forEach(el => el.style.display = 'none');
        }
        
        const roleDisplay = document.getElementById('user-role');
        if (roleDisplay) roleDisplay.textContent = user.role;

    } catch (error) {
        console.error("Failed to load user info", error);
    }
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login.html';
}
