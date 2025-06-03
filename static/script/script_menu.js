function mostrarConteudo(elemento) {
    var formID = elemento.getAttribute('data-form-id');
    var formulario = document.getElementById(formID);

    if (elemento.id === 'menuIcon') {
        // Se o ícone de menu foi clicado, mostre ou oculte o menu sem afetar outros formulários
        var menu = document.getElementById('menu');
        if (menu.style.display === 'block') {
            menu.style.display = 'none';
        } else {
            menu.style.display = 'block';
        }
    } else {
        // Para outros elementos, mostre o formulário e oculte todos os outros
        if (formulario.style.display === 'block') {
            // Se o formulário estiver visível, oculte-o
            formulario.style.display = 'none';
            // Remova a entrada do localStorage
            localStorage.removeItem('formularioAtivo');
        } else {
            // Senão, mostre o formulário e armazene o ID no localStorage
            document.querySelectorAll('.conteudo-escondido').forEach(function(form) {
                if (form.id !== formID) {
                    form.style.display = 'none';
                }
            });
            formulario.style.display = 'block';
            localStorage.setItem('formularioAtivo', formID);
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var formularioAtivo = localStorage.getItem('formularioAtivo');
    if (formularioAtivo) {
        mostrarConteudo(document.querySelector('[data-form-id="' + formularioAtivo + '"]'));
    }
});

function removeFlashMessages() {
    var flashMessages = document.querySelectorAll('.base-alert');
    flashMessages.forEach(function(message) {
        message.style.display = 'none'; // Esconde a mensagem
        // Você pode também remover o elemento completamente com: message.remove();
    });
}

// Chama a função após 5 segundos (5000 milissegundos)
setTimeout(removeFlashMessages, 5000);

document.addEventListener('click', function(event) {
    // Limpar as mensagens flash
    limparMensagensFlash();
});

function limparMensagensFlash() {
    // Remover as mensagens flash do DOM
    document.querySelectorAll('.base-alert').forEach(function(message) {
        message.remove();
    });
}

