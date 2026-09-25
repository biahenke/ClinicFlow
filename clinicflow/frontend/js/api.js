const API_BASE_URL = 'http://localhost:8000/api';

class ApiService {
    static async request(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                ...options,
                headers
            });

            if (response.status === 401) {
                // Token expired or invalid
                localStorage.removeItem('token');
                window.location.href = '/login.html';
                return null;
            }

            if (response.status === 204) {
                return true;
            }

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || 'Ocorreu um erro na requisição');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    static async login(email, password) {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData.toString()
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Falha no login');
        }

        return response.json();
    }

    static async register(data) {
        return this.request('/auth/register', { method: 'POST', body: JSON.stringify(data) });
    }

    static async getMe() {
        return this.request('/auth/me');
    }

    static async getPacientes(skip=0, limit=10) { return this.request(`/pacientes/?skip=${skip}&limit=${limit}`); }
    static async getMedicos(skip=0, limit=10) { return this.request(`/medicos/?skip=${skip}&limit=${limit}`); }
    static async getEspecialidades() { return this.request('/especialidades/'); }
    static async getConsultas(skip=0, limit=10, filters={}) { 
        let url = `/consultas/?skip=${skip}&limit=${limit}`;
        if(filters.data) url += `&data=${filters.data}`;
        if(filters.paciente) url += `&paciente=${filters.paciente}`;
        if(filters.medico) url += `&medico=${filters.medico}`;
        if(filters.especialidade) url += `&especialidade=${filters.especialidade}`;
        if(filters.status) url += `&status=${filters.status}`;
        return this.request(url); 
    }
    static async getHistorico(pacienteId) { return this.request(`/prontuarios/paciente/${pacienteId}`); }

    static async createPaciente(data) { return this.request('/pacientes/', { method: 'POST', body: JSON.stringify(data) }); }
    static async createMedico(data) { return this.request('/medicos/', { method: 'POST', body: JSON.stringify(data) }); }
    static async createConsulta(data) { return this.request('/consultas/', { method: 'POST', body: JSON.stringify(data) }); }
    static async updateConsultaStatus(id, status) { 
        return this.request(`/consultas/${id}/status`, { 
            method: 'PATCH', 
            body: JSON.stringify({ status }) 
        }); 
    }

    // Admin Users
    static async getUsers(skip=0, limit=10, role='') { 
        let url = `/users/?skip=${skip}&limit=${limit}`;
        if(role) url += `&role=${role}`;
        return this.request(url); 
    }
    static async createUserAdmin(data) { return this.request('/users/', { method: 'POST', body: JSON.stringify(data) }); }
    static async updateUserAdmin(id, data) { return this.request(`/users/${id}`, { method: 'PUT', body: JSON.stringify(data) }); }
    static async deleteUserAdmin(id) { return this.request(`/users/${id}`, { method: 'DELETE' }); }
}

window.api = ApiService;

function showToast(message, type = 'success') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div class="toast-icon">${type === 'success' ? '✓' : '✗'}</div>
        <div class="toast-message">${message}</div>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

window.showToast = showToast;

function renderPagination(containerId, totalItems, limit, currentPage, changePageCallback) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = '';
    
    if (totalItems === 0) {
        const totalDiv = document.createElement('div');
        totalDiv.className = 'total-registros';
        totalDiv.textContent = 'Nenhum registro encontrado';
        container.appendChild(totalDiv);
        return;
    }

    const inicio = (currentPage - 1) * limit + 1;
    const fim = Math.min(currentPage * limit, totalItems);

    const totalDiv = document.createElement('div');
    totalDiv.className = 'total-registros';
    totalDiv.innerHTML = `Mostrando <strong>${inicio}</strong> a <strong>${fim}</strong> de <strong>${totalItems}</strong> registros`;
    container.appendChild(totalDiv);

    const totalPages = Math.ceil(totalItems / limit);
    if (totalPages <= 1) return;

    const buttonsContainer = document.createElement('div');
    buttonsContainer.className = 'pagination-buttons';

    const prevBtn = document.createElement('button');
    prevBtn.className = 'page-btn';
    prevBtn.innerHTML = '<i data-lucide="chevron-left" style="width:16px;height:16px;"></i>';
    prevBtn.disabled = currentPage === 1;
    prevBtn.onclick = () => changePageCallback(currentPage - 1);
    buttonsContainer.appendChild(prevBtn);

    const addPageBtn = (page) => {
        const btn = document.createElement('button');
        btn.className = `page-btn ${page === currentPage ? 'active' : ''}`;
        btn.textContent = page;
        btn.onclick = () => changePageCallback(page);
        buttonsContainer.appendChild(btn);
    };

    const addEllipsis = () => {
        const span = document.createElement('span');
        span.textContent = '...';
        span.style.padding = '0 0.5rem';
        span.style.color = 'var(--text-muted)';
        buttonsContainer.appendChild(span);
    };

    addPageBtn(1);
    if (currentPage > 3) addEllipsis();
    if (currentPage > 2) addPageBtn(currentPage - 1);
    if (currentPage !== 1 && currentPage !== totalPages) addPageBtn(currentPage);
    if (currentPage < totalPages - 1) addPageBtn(currentPage + 1);
    if (currentPage < totalPages - 2) addEllipsis();
    if (totalPages > 1) addPageBtn(totalPages);

    const nextBtn = document.createElement('button');
    nextBtn.className = 'page-btn';
    nextBtn.innerHTML = '<i data-lucide="chevron-right" style="width:16px;height:16px;"></i>';
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.onclick = () => changePageCallback(currentPage + 1);
    buttonsContainer.appendChild(nextBtn);

    container.appendChild(buttonsContainer);
    if (window.lucide) window.lucide.createIcons();
}
window.renderPagination = renderPagination;
