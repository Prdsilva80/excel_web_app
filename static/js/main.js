/**
 * Script principal do Sistema de Planilhas
 */

// Função para execução quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa tooltips
    initTooltips();
    
    // Inicializa popovers
    initPopovers();
    
    // Atualiza o ano no rodapé
    updateFooterYear();
    
    // Inicializa manipuladores de formulários
    initFormHandlers();
    
    // Inicializa manipuladores de alertas
    initAlertHandlers();
});

/**
 * Inicializa tooltips do Bootstrap
 */
function initTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Inicializa popovers do Bootstrap
 */
function initPopovers() {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Atualiza o ano no rodapé
 */
function updateFooterYear() {
    const footerYear = document.querySelector('.footer .text-muted');
    if (footerYear) {
        const year = new Date().getFullYear();
        footerYear.innerHTML = footerYear.innerHTML.replace(/\d{4}/, year);
    }
}

/**
 * Inicializa manipuladores de eventos para formulários
 */
function initFormHandlers() {
    // Auto-dismiss para mensagens flash
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-persistent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Confirmação antes de submeter formulários de exclusão
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm(this.getAttribute('data-confirm'))) {
                e.preventDefault();
            }
        });
    });
    
    // Validação de formulários
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Toggle de senha
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            
            // Alterna o ícone
            const icon = this.querySelector('i');
            if (type === 'password') {
                icon.className = 'fas fa-eye';
            } else {
                icon.className = 'fas fa-eye-slash';
            }
        });
    });
}

/**
 * Inicializa manipuladores para alertas
 */
function initAlertHandlers() {
    // Manipulador para fechar alertas
    const closeButtons = document.querySelectorAll('.alert .btn-close');
    closeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            alert.classList.add('fade');
            setTimeout(function() {
                alert.style.display = 'none';
            }, 150);
        });
    });
}

/**
 * Formatação de valores numéricos
 * @param {number} value - Valor a ser formatado
 * @param {number} decimals - Número de casas decimais
 * @param {string} decSeparator - Separador decimal
 * @param {string} thouSeparator - Separador de milhares
 * @returns {string} Valor formatado
 */
function formatNumber(value, decimals = 2, decSeparator = ',', thouSeparator = '.') {
    const fixedValue = parseFloat(value).toFixed(decimals);
    const [intPart, decPart] = fixedValue.split('.');
    
    const formattedIntPart = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, thouSeparator);
    
    return decPart ? `${formattedIntPart}${decSeparator}${decPart}` : formattedIntPart;
}

/**
 * Formata uma data no formato brasileiro
 * @param {string|Date} date - Data a ser formatada
 * @returns {string} Data formatada (dd/mm/aaaa)
 */
function formatDate(date) {
    if (!date) return '';
    
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
        const year = d.getFullYear();
        
        return `${day}/${month}/${year}`;
    }