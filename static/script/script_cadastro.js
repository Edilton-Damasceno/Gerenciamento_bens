function carregarOpcoes() {
    // Faz uma requisição AJAX para o endpoint que retorna as opções
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var opcoes = JSON.parse(this.responseText);
            var select = document.getElementById('modelo');
            opcoes.forEach(function(opcao) {
                var option = document.createElement('option');
                option.text = opcao.text;
                select.appendChild(option);
            });
        }
    };
    xhttp.open('GET', '/api/carrega_opcoes', true);
    xhttp.send();
}
// Chama a função para carregar as opções assim que a página é carregada
window.onload = carregarOpcoes();


function carregarOpcoesSiapeSetor() {
    // Faz uma requisição AJAX para o endpoint que retorna as opções
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var opcoes = JSON.parse(this.responseText);
            var select = document.getElementById('campo-busca');
            opcoes.forEach(function(opcao) {
                var option = document.createElement('option');
                option.text = opcao.text;
                select.appendChild(option);
            });
        }
    };
    xhttp.open('GET', '/api/opcoes', true);
    xhttp.send();
}
window.onload = carregarOpcoesSiapeSetor();


document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/lista_transferencia') // Substitua pelo endpoint do seu backend
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('transferenciaTable').getElementsByTagName('tbody')[0];
            data.forEach(item => {
                const row = tbody.insertRow();
                row.insertCell().textContent = item.patrimonio;
                row.insertCell().textContent = item.modelo;
                row.insertCell().textContent = item.nome;
            });
        })
        .catch(error => console.error('Erro ao carregar dados:', error));
});