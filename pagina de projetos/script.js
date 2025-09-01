document.addEventListener('DOMContentLoaded', () => {
    // Seleciona todos os botões de adicionar item
    const addButtons = document.querySelectorAll('.add-item-btn');

    // Adiciona um ouvinte de evento para cada botão
    addButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            // Encontra a tabela mais próxima do botão que foi clicado
            const taskGroup = event.target.closest('.task-group');
            const tableBody = taskGroup.querySelector('.task-table tbody');

            if (tableBody) {
                // Cria uma nova linha (tr) e suas células (td)
                const newRow = document.createElement('tr');

                newRow.innerHTML = `
                    <td class="task-name" contenteditable="true">Nova Tarefa</td>
                    <td><span class="avatar">S</span></td>
                    <td><div class="status-cell"></div></td>
                    <td></td>
                    <td><div class="priority-cell"></div></td>
                `;

                // Adiciona a nova linha ao corpo da tabela
                tableBody.appendChild(newRow);

                // Foca na nova célula para edição imediata
                newRow.querySelector('.task-name').focus();
            }
        });
    });
});