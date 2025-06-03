document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/patrimonio') // Substitua pelo endpoint do seu backend
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('patrimonioTable').getElementsByTagName('tbody')[0];
            data.forEach(item => {
                const row = tbody.insertRow();
                row.insertCell().textContent = item.patrimonio;
                row.insertCell().textContent = item.modelo;
                row.insertCell().textContent = item.numero_serie;
                row.insertCell().textContent = item.imei_um;
                row.insertCell().textContent = item.imei_dois;
                row.insertCell().textContent = item.setor_siape;
                row.insertCell().textContent = item.estado;
                row.insertCell().textContent = item.localizacao;
                row.insertCell().textContent = item.defeito;
                row.insertCell().textContent = item.observacao;
            });
        })
        .catch(error => console.error('Erro ao carregar dados:', error));
});

document.getElementById('filterInput').addEventListener('keyup', function() {
    const filterValue = this.value.toLowerCase();
    const rows = document.getElementById('patrimonioTable').getElementsByTagName('tr');
    for (let i = 1; i < rows.length; i++) { // Começa em 1 para pular o cabeçalho da tabela
        const cells = rows[i].getElementsByTagName('td');
        let match = false;
        for (let j = 0; j < cells.length; j++) {
            if (cells[j].textContent.toLowerCase().indexOf(filterValue) > -1) {
                match = true;
                break;
            }
        }
        rows[i].style.display = match ? '' : 'none';
    }
});

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/log_transferencia') // Substitua pelo endpoint do seu backend
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('transferenciaTable').getElementsByTagName('tbody')[0];
            data.forEach(item => {
                const row = tbody.insertRow();
                row.insertCell().textContent = item.patrimonio;
                row.insertCell().textContent = item.modelo;
                row.insertCell().textContent = item.numero_serie;
                row.insertCell().textContent = item.imei_um;
                row.insertCell().textContent = item.imei_dois;
                row.insertCell().textContent = item.setor_siape;
                row.insertCell().textContent = item.nome;
                row.insertCell().textContent = item.estado;
                row.insertCell().textContent = item.localizacao;
                row.insertCell().textContent = item.defeito;
                row.insertCell().textContent = item.observacao;
                row.insertCell().textContent = item.data;
            });
        })
        .catch(error => console.error('Erro ao carregar dados:', error));
});

document.getElementById('filterInput_2').addEventListener('keyup', function() {
    const filterValue = this.value.toLowerCase();
    const rows = document.getElementById('transferenciaTable').getElementsByTagName('tr');
    for (let i = 1; i < rows.length; i++) { // Começa em 1 para pular o cabeçalho da tabela
        const cells = rows[i].getElementsByTagName('td');
        let match = false;
        for (let j = 0; j < cells.length; j++) {
            if (cells[j].textContent.toLowerCase().indexOf(filterValue) > -1) {
                match = true;
                break;
            }
        }
        rows[i].style.display = match ? '' : 'none';
    }
});
