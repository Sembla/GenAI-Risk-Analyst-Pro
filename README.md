# 🚀 GenAI Risk Analyst Pro

Assistente de Inteligência Artificial Generativa para análise de crédito, risco e documentos corporativos.

## 🧠 Sobre o projeto

Este projeto simula um cenário real de uso de IA em empresas de dados, crédito e compliance.  
A aplicação usa uma arquitetura RAG simples para recuperar contexto de políticas, contratos e dados do cliente, e pode responder de duas formas:

- **Modo local**: resposta simulada por regras
- **Modo OpenAI**: resposta gerada por LLM com base no contexto recuperado

## ⚙️ Tecnologias

- Python
- Streamlit
- Scikit-learn
- python-dotenv
- OpenAI API
- RAG (Retrieval-Augmented Generation)

## 📂 Estrutura

```bash
genai-risk-analyst-pro/
├── app.py
├── rag.py
├── requirements.txt
├── .env.example
├── README.md
└── data/
    ├── politica_risco.txt
    ├── contrato_credito.txt
    ├── score_cliente.txt
    └── parecer_compliance.txt
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

- Análise de crédito
- Risco e compliance
- Atendimento interno inteligente
- Consulta de políticas corporativas
- Automação de triagem documental

## 📊 Exemplo de uso

**Pergunta:**  
`Esse cliente apresenta risco alto?`

**Resposta esperada:**  
O cliente apresenta alto risco, considerando score abaixo de 600 e histórico de atraso. A política indica necessidade de análise manual antes da aprovação.

## 🔥 Diferencial para currículo

- Arquitetura RAG aplicada a contexto corporativo
- Integração opcional com LLM real
- Interface web em Streamlit
- Organização de base documental e recuperação contextual
- Projeto aderente a cenários de crédito, risco e compliance
