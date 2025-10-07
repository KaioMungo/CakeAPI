const API_BASE_URL = 'http://localhost:5001/cakes';

const form = document.getElementById('cake-form');
const cakeIdInput = document.getElementById('cake-id');
const cakesList = document.getElementById('cakes-list');
const submitBtn = document.getElementById('submit-btn');
const statusMessage = document.getElementById('status-message');


function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = type; // 'success' ou 'error'
    statusMessage.classList.remove('hidden');
    setTimeout(() => {
        statusMessage.classList.add('hidden');
    }, 5000);
}

function resetForm() {
    form.reset();
    cakeIdInput.value = '';
    submitBtn.textContent = 'Cadastrar Bolo';
    submitBtn.style.backgroundColor = '#4CAF50';
}

// --- Funções de Interação com a API ---

// 1. READ (GET) - Carrega todos os bolos
async function fetchCakes() {
    try {
        const response = await fetch(API_BASE_URL);
        const cakes = await response.json();
        
        cakesList.innerHTML = ''; // Limpa a lista
        
        if (cakes.length === 0) {
            cakesList.innerHTML = '<p>Nenhum bolo cadastrado. Use o formulário acima para adicionar um!</p>';
            return;
        }

        cakes.forEach(cake => {
            const card = createCakeCard(cake);
            cakesList.appendChild(card);
        });

    } catch (error) {
        showStatus('Erro ao carregar bolos: A API está rodando?', 'error');
        console.error('Fetch error:', error);
    }
}

// 2. CREATE (POST) / UPDATE (PUT) - Envia o formulário
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const id = cakeIdInput.value;
    const isUpdating = id !== '';
    const method = isUpdating ? 'PUT' : 'POST';
    const url = isUpdating ? `${API_BASE_URL}/${id}` : API_BASE_URL;

    const cakeData = {
        name: document.getElementById('name').value,
        flavor: document.getElementById('flavor').value,
        price: parseFloat(document.getElementById('price').value),
        description: document.getElementById('description').value
    };

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(cakeData),
        });

        if (response.ok) {
            showStatus(`Bolo ${isUpdating ? 'atualizado' : 'cadastrado'} com sucesso!`, 'success');
            resetForm();
            fetchCakes();
        } else {
            const errorData = await response.json();
            showStatus(`Erro (${response.status}): ${errorData.message || 'Falha na operação.'}`, 'error');
        }

    } catch (error) {
        showStatus('Erro de conexão com o servidor. Verifique o console.', 'error');
        console.error('Submit error:', error);
    }
});


// 3. DELETE - Deleta um bolo
async function deleteCake(id) {
    if (!confirm('Tem certeza que deseja deletar este bolo?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/${id}`, {
            method: 'DELETE',
        });

        if (response.status === 204) { // 204 No Content é o padrão para DELETE bem-sucedido
            showStatus('Bolo deletado com sucesso!', 'success');
            fetchCakes();
        } else {
            showStatus(`Erro (${response.status}): Falha ao deletar.`, 'error');
        }

    } catch (error) {
        showStatus('Erro de conexão ao deletar.', 'error');
        console.error('Delete error:', error);
    }
}

// 4. PREENCHER FORMULÁRIO para Edição
function editCake(cake) {
    cakeIdInput.value = cake.id;
    document.getElementById('name').value = cake.name;
    document.getElementById('flavor').value = cake.flavor;
    document.getElementById('price').value = cake.price;
    document.getElementById('description').value = cake.description;

    submitBtn.textContent = 'Atualizar Bolo';
    submitBtn.style.backgroundColor = '#ffc107'; 
    window.scrollTo(0, 0); // Rola para o topo para ver o formulário
}


// --- Geração do HTML ---
function createCakeCard(cake) {
    const div = document.createElement('div');
    div.className = 'cake-card';
    
    // Formata o preço para BRL
    const formattedPrice = new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(cake.price);

    div.innerHTML = `
        <div>
            <h3>${cake.name} (ID: ${cake.id})</h3>
            <p>Sabor: ${cake.flavor}</p>
            <p>Disponível: ${cake.available || 'Sim'}</p>
            <p>${cake.description || 'Sem descrição.'}</p>
        </div>
        <div>
            <p class="price">${formattedPrice}</p>
            <div class="actions">
                <button class="edit-btn">Editar</button>
                <button class="delete-btn">Deletar</button>
            </div>
        </div>
    `;

    // Adiciona event listeners aos botões
    div.querySelector('.edit-btn').addEventListener('click', () => editCake(cake));
    div.querySelector('.delete-btn').addEventListener('click', () => deleteCake(cake.id));

    return div;
}

// Inicia o carregamento dos dados ao abrir a página
fetchCakes();