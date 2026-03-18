import streamlit as st
from insights import carregar_dados, gerar_kpis, responder_pergunta, gerar_resumo

st.set_page_config(page_title="Data Insight AI", layout="wide", page_icon="📊")

st.title("📊 Data Insight AI")
st.caption("Análise de indicadores de negócio com IA Generativa")

# Carregar dados
df = carregar_dados("data/vendas.csv")

with st.sidebar:
    st.header("🎯 Filtros de Análise")
    regioes = ["Todas"] + sorted(df["regiao"].unique().tolist())
    categorias = ["Todas"] + sorted(df["categoria"].unique().tolist())

    regiao = st.selectbox("Selecione a Região", regioes)
    categoria = st.selectbox("Selecione a Categoria", categorias)
    
    st.divider()
    usar_llm = st.toggle("Usar Inteligência Artificial (OpenAI)", value=True)
    st.info("Ative para análises mais complexas e naturais.")

# Aplicar Filtros
df_filtrado = df.copy()
if regiao != "Todas":
    df_filtrado = df_filtrado[df_filtrado["regiao"] == regiao]
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria"] == categoria]

# Exibição de KPIs
kpis = gerar_kpis(df_filtrado)
col1, col2, col3 = st.columns(3)
col1.metric("Faturamento", f"R$ {kpis['faturamento']:,.2f}")
col2.metric("Pedidos", int(kpis["pedidos"]))
col3.metric("Ticket Médio", f"R$ {kpis['ticket_medio']:,.2f}")

st.divider()

# Layout em duas colunas para Resumo e Tabela
c_data, c_sum = st.columns([2, 1])

with c_data:
    st.subheader("📋 Dados Selecionados")
    st.dataframe(df_filtrado, use_container_width=True, height=300)

with c_sum:
    st.subheader("💡 Insight Rápido")
    st.success(gerar_resumo(df_filtrado))

# Pergunta ao usuário
st.divider()
st.subheader("💬 Explore os dados em linguagem natural")
pergunta = st.text_input("Pergunta", placeholder="Ex: Qual região teve o maior ticket médio?")

if pergunta:
    with st.spinner("Analisando base de dados..."):
        resposta, modo = responder_pergunta(df_filtrado, pergunta, usar_llm=usar_llm)
        st.chat_message("assistant").write(resposta)
        st.caption(f"Mecanismo: {modo}")

st.markdown("---")
st.caption("Desenvolvido por Henrique Sembla")