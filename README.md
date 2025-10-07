# 🎂 Sistema de Gestão de Pedidos para Confeitaria (Cake Ordering API)

## 📝 Propósito e Ideia Geral da Aplicação

Este projeto é uma **API RESTful** desenvolvida para gerenciar o catálogo de produtos e o fluxo de pedidos de uma confeitaria ou pequeno negócio de bolos.

### A Quem Se Destina
* **Confeitarias e Padeiros:** Proprietários que precisam de um sistema para registrar seu catálogo de produtos (bolos), gerenciar informações de clientes e rastrear pedidos em andamento.
* **Desenvolvedores:** Como *backend* para futuras aplicações (web ou mobile) de vendas, facilitando a interação e o processamento de dados transacionais.

### O Que Se Pretende Fazer
O objetivo principal é digitalizar e centralizar o processo de vendas. A API permite:
1.  **CRUD (Create, Read, Update, Delete)** de **Bolos** (produtos).
2.  **CRUD** de **Clientes**.
3.  Gerenciamento do ciclo de vida de **Pedidos**, desde a criação até a entrega, ligando clientes a produtos.

---

## 🛠️ Stack e Tecnologias Utilizadas no Projeto

A aplicação foi desenvolvida utilizando uma stack moderna e popular em Python:

| Categoria | Tecnologia | Versão Principal |
| :--- | :--- | :--- |
| **Linguagem** | Python | 3.x |
| **Framework Web** | Flask | Latest |
| **ORM (Mapeamento Objeto-Relacional)** | Flask-SQLAlchemy | Latest |
| **Banco de Dados** | SQLite (padrão para desenvolvimento) | - |
| **Gerenciador de Dependências** | pip | 

---

## 🚀 Como Rodar a API Localmente

Siga os comandos abaixo para configurar e iniciar o servidor da API.

### Pré-requisitos
Certifique-se de ter o **Python 3.x** e o **pip** instalados.

### 1. Clonar o Repositório
```bash
git clone [URL_DO_SEU_REPOSITORIO]
cd [BackEnd]

# Cria o ambiente virtual
python -m venv venv
# Ativa o ambiente virtual (Linux/macOS)
source venv/bin/activate
# Ativa o ambiente virtual (Windows)
venv\Scripts\activate

pip install -r requirements.txt 
# (ou instale individualmente se não tiver requirements.txt: pip install flask flask-sqlalchemy)

📐 Diagrama Entidade-Relacionamento (ERD)
O modelo de dados é relacional e utiliza uma tabela de ligação (order_items) para resolver o relacionamento de Muitos para Muitos (N:M) entre Bolos e Pedidos.

Entidades (Tabelas)

cakes: Cadastro de produtos (Bolos).

customers: Cadastro de Clientes.

orders: Registro das transações (Pedidos).

order_items: Tabela de ligação que detalha quais bolos e em que quantidade estão em cada pedido.
