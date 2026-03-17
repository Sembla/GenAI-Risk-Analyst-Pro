# 🚀 GenAI Risk Analyst Pro

> 💡 Projeto inspirado em aplicações reais de IA utilizadas em empresas como Serasa Experian para análise de crédito, risco e compliance.

Assistente de Inteligência Artificial Generativa para análise de crédito, risco e documentos corporativos.

## 🎯 Objetivo

Demonstrar na prática a aplicação de IA Generativa em cenários de negócio, integrando dados, automação e inteligência para apoio à análise de risco e tomada de decisão.

## 🧠 Sobre o projeto

Este projeto simula um cenário real de aplicação de Inteligência Artificial Generativa em ambientes corporativos, especialmente nos contextos de crédito, risco e compliance.

A solução utiliza arquitetura RAG (Retrieval-Augmented Generation) para recuperação contextual de informações e geração de respostas inteligentes, permitindo apoio à tomada de decisão baseada em dados.

A aplicação pode responder de duas formas:

* **Modo local**: resposta simulada por regras
* **Modo OpenAI**: resposta gerada por LLM com base no contexto recuperado

## ⚙️ Tecnologias

* Python
* Streamlit
* Scikit-learn
* python-dotenv
* OpenAI API
* RAG (Retrieval-Augmented Generation)

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

* Análise de crédito
* Risco e compliance
* Atendimento interno inteligente
* Consulta de políticas corporativas
* Automação de triagem documental

## 📊 Exemplo de uso

**Pergunta:**

> Esse cliente apresenta risco alto com base na política?

**Resposta esperada:**
O cliente apresenta alto risco, considerando score abaixo de 600 e histórico de atraso. A política indica necessidade de análise manual antes da aprovação.

## 🏗️ Arquitetura da Solução

1. Ingestão de documentos (políticas, contratos e dados)
2. Processamento e vetorização (TF-IDF)
3. Recuperação de contexto relevante (RAG)
4. Geração de resposta:

   * Modo local (regra)
   * Modo LLM (OpenAI)
5. Interface web para interação do usuário

## 📈 Possíveis Evoluções

* Integração com banco vetorial (FAISS / Pinecone)
* Implementação de embeddings semânticos
* Deploy em ambiente cloud (AWS / Azure)
* Integração com APIs externas de score de crédito
* Monitoramento e avaliação de respostas (LLM Observability)

## 👨‍💻 Autor

**Henrique Sembla**
🔗 GitHub: https://github.com/Sembla
📍 São Paulo – Brasil

Especialista em desenvolvimento de soluções com IA Generativa, com foco em automação, dados e aplicações corporativas.
