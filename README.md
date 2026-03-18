# 📊 Data Insight AI

> 💡 Projeto de IA aplicada à análise de dados, permitindo que usuários façam perguntas em linguagem natural e recebam respostas com base em indicadores de negócio.

Assistente de análise de dados com interface web, filtros interativos e respostas automáticas com apoio de LLM ou regras locais.

## 🎯 Objetivo

Demonstrar uma aplicação prática de IA para exploração de dados, unindo visualização, métricas de negócio e perguntas em linguagem natural.

## 🧠 Sobre o projeto

O sistema carrega uma base de vendas, calcula KPIs e permite que o usuário pergunte coisas como:

* Qual categoria vende mais?
* Qual região tem maior faturamento?
* Qual é o ticket médio?
* Qual o faturamento total?

A aplicação pode responder de duas formas:

* **Modo local**: respostas baseadas em regras
* **Modo OpenAI**: respostas geradas por LLM com base nos dados filtrados

## ⚙️ Tecnologias

* Python
* Streamlit
* Pandas
* python-dotenv
* OpenAI API

## 📂 Estrutura

```bash
data-insight-ai/
├── app.py
├── insights.py
├── requirements.txt
├── .env.example
├── README.md
└── data/
    └── vendas.csv
```

## ▶️ Como executar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente
Crie um arquivo `.env` com base no `.env.example`.

### 3. Rodar a aplicação
```bash
streamlit run app.py
```

## 🔐 Variáveis de ambiente

```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4o-mini
```

## 💼 Aplicações

* Business Intelligence com IA
* Exploração de dados em linguagem natural
* Dashboards explicativos
* Apoio à tomada de decisão
* Assistentes analíticos para times de negócio

## 📊 Exemplo de perguntas

* Qual categoria vende mais?
* Qual região tem maior faturamento?
* Qual é o ticket médio?
* Qual o faturamento total?

## 👨‍💻 Autor

**Henrique Sembla**  
🔗 GitHub: https://github.com/Sembla
