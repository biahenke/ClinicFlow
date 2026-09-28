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
        return this.request('/users/me');
    }

    static async updateMe(data) {
        return this.request('/users/me', { method: 'PUT', body: JSON.stringify(data) });
    }

    static async changePassword(data) {
        return this.request('/auth/change-password', { method: 'PUT', body: JSON.stringify(data) });
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
    static async updatePaciente(id, data) { return this.request(`/pacientes/${id}`, { method: 'PUT', body: JSON.stringify(data) }); }
    static async createMedico(data) { return this.request('/medicos/', { method: 'POST', body: JSON.stringify(data) }); }
    static async updateMedico(id, data) { return this.request(`/medicos/${id}`, { method: 'PUT', body: JSON.stringify(data) }); }
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

    // Relatorios
    static async getRelatoriosSummary(filters={}) { 
        const params = new URLSearchParams();
        if(filters.start_date) params.append('start_date', filters.start_date);
        if(filters.end_date) params.append('end_date', filters.end_date);
        
        const queryString = params.toString();
        const url = `/relatorios/summary${queryString ? '?' + queryString : ''}`;
        return this.request(url); 
    }
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
    container.className = 'flex flex-col sm:flex-row items-center justify-between gap-4 p-4 border-t border-[#1e293b] text-sm text-slate-400 mt-2';
    
    if (totalItems === 0) {
        const totalDiv = document.createElement('div');
        totalDiv.textContent = 'Nenhum registro encontrado';
        container.appendChild(totalDiv);
        return;
    }

    const inicio = (currentPage - 1) * limit + 1;
    const fim = Math.min(currentPage * limit, totalItems);

    const totalDiv = document.createElement('div');
    totalDiv.innerHTML = `Mostrando <strong class="text-white font-medium">${inicio}</strong> a <strong class="text-white font-medium">${fim}</strong> de <strong class="text-white font-medium">${totalItems}</strong> registros`;
    container.appendChild(totalDiv);

    const totalPages = Math.ceil(totalItems / limit);
    if (totalPages <= 1) return;

    const buttonsContainer = document.createElement('div');
    buttonsContainer.className = 'flex items-center gap-1';

    const createBtn = (content, disabled, onClick, isActive = false) => {
        const btn = document.createElement('button');
        btn.innerHTML = content;
        btn.disabled = disabled;
        
        let classes = 'w-8 h-8 flex items-center justify-center rounded-lg text-sm font-medium transition-all duration-200 ';
        
        if (isActive) {
            classes += 'bg-sky-600 text-white shadow-lg shadow-sky-500/30';
        } else if (disabled) {
            classes += 'text-slate-600 cursor-not-allowed';
        } else {
            classes += 'text-slate-400 hover:text-white hover:bg-[#1e293b] border border-transparent hover:border-[#334155]';
        }
        
        btn.className = classes;
        if (!disabled && onClick) {
            btn.onclick = onClick;
        }
        return btn;
    };

    const prevBtn = createBtn('<i class="ph ph-caret-left text-lg"></i>', currentPage === 1, () => changePageCallback(currentPage - 1));
    buttonsContainer.appendChild(prevBtn);

    const addPageBtn = (page) => {
        buttonsContainer.appendChild(createBtn(page, false, () => changePageCallback(page), page === currentPage));
    };

    const addEllipsis = () => {
        const span = document.createElement('span');
        span.textContent = '...';
        span.className = 'text-slate-500 px-1';
        buttonsContainer.appendChild(span);
    };

    addPageBtn(1);
    if (currentPage > 3) addEllipsis();
    if (currentPage > 2) addPageBtn(currentPage - 1);
    if (currentPage !== 1 && currentPage !== totalPages) addPageBtn(currentPage);
    if (currentPage < totalPages - 1) addPageBtn(currentPage + 1);
    if (currentPage < totalPages - 2) addEllipsis();
    if (totalPages > 1) addPageBtn(totalPages);

    const nextBtn = createBtn('<i class="ph ph-caret-right text-lg"></i>', currentPage === totalPages, () => changePageCallback(currentPage + 1));
    buttonsContainer.appendChild(nextBtn);

    container.appendChild(buttonsContainer);
}
window.renderPagination = renderPagination;
