import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def carregar_dados(caminho: str) -> pd.DataFrame:
    """Carrega o CSV e garante que os dados básicos existam."""
    if not os.path.exists(caminho):
        # Fallback para teste inicial se o arquivo não estiver na pasta
        return pd.DataFrame({
            'pedido_id': [1, 2, 3],
            'categoria': ['Eletrônicos', 'Moda', 'Home'],
            'regiao': ['Sul', 'Norte', 'Sudeste'],
            'valor_total': [1200.0, 450.0, 800.0]
        })
    return pd.read_csv(caminho)

def gerar_kpis(df: pd.DataFrame) -> dict:
    """Calcula métricas principais com segurança."""
    if df.empty:
        return {"faturamento": 0.0, "pedidos": 0, "ticket_medio": 0.0}
    
    faturamento = float(df["valor_total"].sum())
    pedidos = int(df["pedido_id"].nunique())
    ticket_medio = faturamento / pedidos if pedidos > 0 else 0
    return {
        "faturamento": faturamento,
        "pedidos": pedidos,
        "ticket_medio": ticket_medio
    }

def gerar_resumo(df: pd.DataFrame) -> str:
    """Gera um texto executivo baseado nos dados filtrados."""
    if df.empty:
        return "Nenhum dado encontrado para os filtros selecionados."

    top_categoria = df.groupby("categoria")["valor_total"].sum().idxmax()
    top_regiao = df.groupby("regiao")["valor_total"].sum().idxmax()
    total = df["valor_total"].sum()

    return (
        f"Análise Consolidada: O faturamento total sob esses filtros é de R$ {total:,.2f}. "
        f"A categoria '{top_categoria}' é a líder de vendas, e a região '{top_regiao}' apresenta o maior volume financeiro."
    )

def _resposta_regra(df: pd.DataFrame, pergunta: str) -> str:
    """Lógica local por palavras-chave (sem custo de API)."""
    p = pergunta.lower()
    if df.empty: return "Base de dados vazia."

    if "categoria" in p:
        res = df.groupby("categoria")["valor_total"].sum().sort_values(ascending=False)
        return f"A categoria com maior faturamento é {res.index[0]} (R$ {res.iloc[0]:,.2f})."

    if "regiao" in p or "região" in p:
        res = df.groupby("regiao")["valor_total"].sum().sort_values(ascending=False)
        return f"A região com maior resultado é {res.index[0]} (R$ {res.iloc[0]:,.2f})."

    if "ticket" in p:
        kpis = gerar_kpis(df)
        return f"O ticket médio atual é de R$ {kpis['ticket_medio']:,.2f}."

    if "faturamento" in p or "total" in p:
        total = df["valor_total"].sum()
        return f"O faturamento total acumulado é de R$ {total:,.2f}."

    return "Não entendi sua pergunta no modo local. Tente perguntar sobre faturamento, regiões ou categorias."

def _resposta_openai(df: pd.DataFrame, pergunta: str) -> str:
    """Análise via LLM (OpenAI) com contexto otimizado."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não configurada no .env")

    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    # Enviamos apenas os KPIs e uma amostra para economizar tokens e ser preciso
    kpis = gerar_kpis(df)
    amostra = df.head(10).to_csv(index=False)

    prompt = f"""
    Você é um Analista de BI. Responda em Português (BR).
    Dados Consolidados: Faturamento R$ {kpis['faturamento']:.2f}, Pedidos {kpis['pedidos']}, Ticket Médio R$ {kpis['ticket_medio']:.2f}.
    Amostra (CSV):
    {amostra}

    Pergunta: {pergunta}
    Responda de forma direta e profissional.
    """

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "system", "content": "Você é um assistente de análise de dados."},
                  {"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()

def responder_pergunta(df: pd.DataFrame, pergunta: str, usar_llm: bool = True):
    """Orquestra a resposta entre IA ou Regras."""
    if usar_llm:
        try:
            return _resposta_openai(df, pergunta), "OpenAI (GPT)"
        except Exception as e:
            return _resposta_regra(df, pergunta), f"Local (Erro na API: {str(e)})"
    return _resposta_regra(df, pergunta), "Local (Regras)"