document.addEventListener('DOMContentLoaded', () => {
    const toggleButtons = document.querySelectorAll('.btn-view');
    
    toggleButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const input = document.getElementById(this.dataset.target);
            if (input.type === 'password') {
                input.type = 'text';
                this.textContent = 'Ocultar';
                this.style.color = 'var(--primary)';
            } else {
                input.type = 'password';
                this.textContent = 'Ver';
                this.style.color = 'var(--text-muted)';
            }
        });
    });

    const form = document.getElementById('formCadastro');
    if (form) {
        form.addEventListener('submit', (e) => {
            const p1 = document.getElementById('pass1').value;
            const p2 = document.getElementById('pass2').value;

            if (p1 !== p2) {
                e.preventDefault();
                alert('Atenção: As senhas digitadas não são iguais.');
            }
        });
    }
});
