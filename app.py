import streamlit as st
from rag import carregar_documentos, buscar_contexto, gerar_resposta

st.set_page_config(page_title="GenAI Risk Analyst Pro", layout="wide")

st.title("🤖 GenAI Risk Analyst Pro")
st.caption("Assistente de IA Generativa para análise de crédito, risco e documentos")

with st.sidebar:
    st.header("Configurações")
    usar_llm = st.toggle("Usar OpenAI (se configurado)", value=True)
    top_k = st.slider("Quantidade de trechos recuperados", 1, 3, 2)
    st.markdown(
        """
        **Exemplos de perguntas**
        - Esse cliente apresenta risco alto?
        - O score permite aprovação automática?
        - Quando a análise manual é obrigatória?
        """
    )

documentos = carregar_documentos("data")

col1, col2 = st.columns([1.3, 1])

with col1:
    pergunta = st.text_area("Digite sua pergunta", height=120, placeholder="Ex: Esse cliente apresenta risco alto?")
    enviar = st.button("Analisar")

with col2:
    st.subheader("Base carregada")
    st.write(f"{len(documentos)} documento(s) disponível(is).")

if enviar and pergunta.strip():
    contexto = buscar_contexto(pergunta, documentos, top_k=top_k)
    resposta, modo = gerar_resposta(pergunta, contexto, usar_llm=usar_llm)

    st.subheader("📊 Resposta")
    st.write(resposta)

    with st.expander("Contexto recuperado"):
        st.code(contexto)

    st.caption(f"Modo de resposta: {modo}")
