
import streamlit as st
import pandas as pd
from datetime import datetime
import os
from fpdf import FPDF

# Configuração da página
st.set_page_config(page_title="Causa Raiz", layout="centered", initial_sidebar_state="collapsed")

st.markdown("## 🧠 Causa Raiz")
st.markdown("### Desenvolvido por Paulo Amoroso")
st.markdown("---")

# Inicializa o DataFrame
DATA_FILE = "problemas.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Data", "Título", "Categoria", "Descrição", "Porquê 1", "Porquê 2", "Porquê 3", "Porquê 4", "Porquê 5", "Causa Raiz", "Ação Corretiva", "Responsável", "Prazo"])

# Inicializa valores padrão no session_state
valores_iniciais = {
    "titulo": "",
    "categoria": "Qualidade",
    "descricao": "",
    "pq1": "",
    "pq2": "",
    "pq3": "",
    "pq4": "",
    "pq5": "",
    "causa_raiz": "",
    "acao": "",
    "responsavel": "",
    "prazo": datetime.today(),
    "resetar": False
}
for campo, valor in valores_iniciais.items():
    if campo not in st.session_state:
        st.session_state[campo] = valor

# Formulário de entrada
with st.form("registro_problema"):
    st.subheader("📋 Registrar Novo Problema")
    titulo = st.text_input("Título do Problema", key="titulo")
    categoria = st.selectbox("Categoria", ["Qualidade", "Segurança", "Prazo", "Custo", "Outro"], key="categoria")
    descricao = st.text_area("Descrição do Problema", key="descricao")
    pq1 = st.text_input("Por quê 1?", key="pq1")
    pq2 = st.text_input("Por quê 2?", key="pq2")
    pq3 = st.text_input("Por quê 3?", key="pq3")
    pq4 = st.text_input("Por quê 4?", key="pq4")
    pq5 = st.text_input("Por quê 5?", key="pq5")
    causa_raiz = st.text_area("Causa Raiz Identificada", key="causa_raiz")
    acao = st.text_input("Ação Corretiva Sugerida", key="acao")
    responsavel = st.text_input("Responsável", key="responsavel")
    prazo = st.date_input("Prazo para Ação", key="prazo")

    submitted = st.form_submit_button("Salvar Registro")

    if submitted:
        nova_linha = {
            "Data": datetime.today().strftime("%Y-%m-%d"),
            "Título": titulo,
            "Categoria": categoria,
            "Descrição": descricao,
            "Porquê 1": pq1,
            "Porquê 2": pq2,
            "Porquê 3": pq3,
            "Porquê 4": pq4,
            "Porquê 5": pq5,
            "Causa Raiz": causa_raiz,
            "Ação Corretiva": acao,
            "Responsável": responsavel,
            "Prazo": prazo
        }
        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Problema registrado com sucesso!")

        # Sinaliza para limpar fora do form
        st.session_state.resetar = True

# Executa limpeza fora do formulário, após o rerun
if st.session_state.resetar:
    for campo in ["titulo", "categoria", "descricao", "pq1", "pq2", "pq3", "pq4", "pq5", "causa_raiz", "acao", "responsavel"]:
        st.session_state[campo] = ""
    st.session_state["prazo"] = datetime.today()
    st.session_state.resetar = False
    st.rerun()

# Histórico e PDF
st.markdown("---")
st.subheader("📚 Histórico de Problemas Registrados")
if df.empty:
    st.info("Nenhum problema registrado ainda.")
else:
    st.dataframe(df.tail(10), use_container_width=True)

    # Última entrada
    ultimo = df.iloc[-1]

    # Diagrama textual
    st.markdown("### 🔍 Diagrama dos 5 Porquês")
    st.markdown(f'''
**Problema:** {ultimo["Descrição"]}  
⬇️  
**1️⃣ Por quê?** {ultimo["Porquê 1"]}  
⬇️  
**2️⃣ Por quê?** {ultimo["Porquê 2"]}  
⬇️  
**3️⃣ Por quê?** {ultimo["Porquê 3"]}  
⬇️  
**4️⃣ Por quê?** {ultimo["Porquê 4"]}  
⬇️  
**5️⃣ Por quê?** {ultimo["Porquê 5"]}  
''')

    # Gerar PDF
    def gerar_pdf(entrada):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Relatório - Causa Raiz", ln=True)

        pdf.set_font("Arial", "", 12)
        for k, v in entrada.items():
            pdf.multi_cell(0, 10, f"{k}: {v}")
        pdf.output("relatorio_ultima_analise.pdf")

    if st.button("📄 Gerar PDF da Última Análise"):
        gerar_pdf(ultimo)
        with open("relatorio_ultima_analise.pdf", "rb") as f:
            st.download_button("📥 Baixar PDF", f, file_name="causa_raiz_analise.pdf")
