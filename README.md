# Solução do Desafio Nola (Nola Challenge Solution)

Este repositório contém a solução completa para o "Nola Challenge". É uma aplicação web full-stack que inclui um dashboard interativo (frontend) e uma API para fornecimento de dados (backend).

## Stack de Tecnologia

Este projeto utiliza uma arquitetura moderna separando o backend do frontend.

**Backend:**
* **Python 3**
* **FastAPI:** Para a criação da API REST.
* **Pydantic:** Para validação de dados e schemas.
* **SQLAlchemy:** (Inferido) Para interação com a base de dados.

**Frontend:**
* **Nuxt.js 3:** Framework baseada em Vue.js.
* **Vue.js:** Para a construção da interface de utilizador.
* **TypeScript:** Para tipagem de código no frontend.
* **Componentes de Gráfico:** Visualização de dados (ex: Gráficos de Barra e Linha).
* **Componentes de Dashboard:** (ex: KpiCard, InfoList).

## Estrutura do Projeto

nola-challenge-solution/

├── .gitignore

├── backend/

│ ├── database.py

│ ├── main.py # Ponto de entrada da API (FastAPI)

│ ├── requirements.txt # Dependências do Python

│ └── schemas.py # Schemas Pydantic (validação)

├── docs/

│ └── adr/ # Documentação (Architecture Decision Records)

│ ├── 001-visao-geral-da-solucao.md

│ ├── 002-escolha-do-stack.md

│ ├── 003-arquitetura-da-api.md

│ ├── 004-estrategia-de-filtros.md

│ ├── 005-organizacao-da-ui.md

│ └── 006-funcionalidades-extras.md

└── frontend/

├── components/ # Componentes Vue reutilizáveis

│ ├── BarChart.vue

│ ├── InfoList.vue

│ ├── KpiCard.vue

│ └── LineChart.vue

├── public/ # Ficheiros estáticos (ícones, etc.)

│ ├── favicon.ico

│ └── robots.txt

├── .gitignore

├── app.vue # Componente principal da página

├── nuxt.config.ts # Configuração do Nuxt.js

├── package.json # Dependências do Node.js

├── package-lock.json

├── README.md

└── tsconfig.json # Configuração do TypeScript

## Instalação e Execução

Para executar este projeto localmente, segue os passos abaixo.

**Pré-requisitos:**
* Python 3.8+
* Node.js v18+ (e npm)

### 1. Backend (API)

Recomenda-se o uso de um ambiente virtual (virtualenv) para o backend.

```bash
# 1. Navega para a pasta do backend
cd backend

# 2. (Opcional, mas recomendado) Cria e ativa um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: .\venv\Scripts\activate

# 3. Instala as dependências Python
pip install -r requirements.txt

# 4. Executa o servidor da API (com hot-reload)
# O FastAPI será servido em [http://127.0.0.1:8000](http://127.0.0.1:8000)
uvicorn main:app --reload
```
### 2. Frontend (Dashboard)

Abre um novo terminal para executar o frontend.

```bash
# 1. Navega para a pasta do frontend
cd frontend

# 2. Instala as dependências do Node.js
npm install

# 3. Executa o servidor de desenvolvimento do Nuxt.js
# A aplicação estará disponível em http://localhost:3000
npm run dev
```

## Documentação (ADRs)
As decisões de arquitetura e design deste projeto estão documentadas na pasta docs/adr/.

001-visao-geral-da-solucao.md

002-escolha-do-stack.md

003-arquitetura-da-api.md

004-estrategia-de-filtros.md

005-organizacao-da-ui.md

006-funcionalidades-extras.md

## Visualização

Uma pré-visualização do dashboard principal da aplicação.

<img width="1919" height="895" alt="Captura de tela 2025-11-03 191745" src="https://github.com/user-attachments/assets/56e3b219-6f68-4dfe-8b42-db780641e6a1" />
<img width="1919" height="861" alt="Captura de tela 2025-11-03 191756" src="https://github.com/user-attachments/assets/7d04e135-c050-4358-95c5-1abd6bc1624c" />
<img width="1919" height="852" alt="Captura de tela 2025-11-03 191804" src="https://github.com/user-attachments/assets/60c30e4b-0ca3-423a-ac1f-b2c9b8e3dba1" />
