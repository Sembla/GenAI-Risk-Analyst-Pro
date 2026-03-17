import os
from pathlib import Path
from typing import List, Tuple

from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()


def carregar_documentos(pasta: str) -> List[str]:
    docs = []
    for arquivo in sorted(os.listdir(pasta)):
        caminho = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                docs.append(f"[{arquivo}]\n" + f.read())
    return docs


def buscar_contexto(pergunta: str, documentos: List[str], top_k: int = 2) -> str:
    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(documentos)
    pergunta_vec = vectorizer.transform([pergunta])

    similaridades = cosine_similarity(pergunta_vec, doc_vectors).flatten()
    indices = similaridades.argsort()[::-1][:top_k]
    melhores = [documentos[i] for i in indices]
    return "\n\n---\n\n".join(melhores)


def _resposta_regra(pergunta: str, contexto: str) -> str:
    texto = contexto.lower()
    if "580" in texto or "abaixo de 600" in texto:
        classificacao = "alto risco"
    elif "entre 600 e 750" in texto:
        classificacao = "risco moderado"
    else:
        classificacao = "risco não identificado com precisão"

    analise_manual = "sim" if "análise manual" in texto or "analise manual" in texto else "não identificado"

    return (
        f"Com base nos documentos recuperados, o caso indica **{classificacao}**. "
        f"A necessidade de análise manual aparece como **{analise_manual}** nos critérios consultados. "
        f"Recomendação: validar score, histórico de pagamentos e política vigente antes da decisão final."
    )


def _resposta_openai(pergunta: str, contexto: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não configurada.")

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    prompt = f"""
Você é um analista de risco corporativo.
Responda em português do Brasil, de forma objetiva e profissional.

Pergunta do usuário:
{pergunta}

Contexto recuperado:
{contexto}

Regras:
- Use apenas o contexto fornecido.
- Se faltar informação, diga isso claramente.
- Indique classificação de risco quando possível.
- Traga recomendação final em 1 frase.
"""
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "Você é um assistente especialista em crédito, risco e compliance."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def gerar_resposta(pergunta: str, contexto: str, usar_llm: bool = True) -> Tuple[str, str]:
    if usar_llm:
        try:
            return _resposta_openai(pergunta, contexto), "OpenAI"
        except Exception:
            pass
    return _resposta_regra(pergunta, contexto), "Simulação local"
