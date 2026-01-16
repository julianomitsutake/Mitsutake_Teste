# # titulo
# # input do chat
# # a cada mensagem enviada:
#     # mostrar a mensagem que o usuario enviou no chat
#     # enviar essa mensagem para a IA responder
#     # aparece na tela a resposta da IA

# # streamlit - frontend e backend

# # rodar streamlit run main.py
# # streamlit run "C:\Users\jm800945\Desktop\Python Autogui - 13-01-2026\Aula 4\main.py"
# import streamlit as st
# from openai import OpenAI

# modelo = OpenAI(api_key="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")

# st.write("### ChatBot com IA") # markdown

# # session_state = memoria do streamlit
# if not "lista_mensagens" in st.session_state:
#     st.session_state["lista_mensagens"] = []

# # adicionar uma mensagem
# # st.session_state["lista_mensagens"].append(mensagem)

# # exibir o histórico de mensagens
# for mensagem in st.session_state["lista_mensagens"]:
#     role = mensagem["role"]
#     content = mensagem["content"]
#     st.chat_message(role).write(content)

# mensagem_usuario = st.chat_input("Escreva sua mensagem aqui")

# if mensagem_usuario:
#     # user -> ser humano
#     # assistant -> inteligencia artificial
#     st.chat_message("user").write(mensagem_usuario)
#     mensagem = {"role": "user", "content": mensagem_usuario}
#     st.session_state["lista_mensagens"].append(mensagem)

#     # resposta da IA
#     resposta_modelo = modelo.chat.completions.create(
#         messages=st.session_state["lista_mensagens"],
#         model="gpt-4o"
#     )
    
#     resposta_ia = resposta_modelo.choices[0].message.content

#     # exibir a resposta da IA na tela
#     st.chat_message("assistant").write(resposta_ia)
#     mensagem_ia = {"role": "assistant", "content": resposta_ia}
#     st.session_state["lista_mensagens"].append(mensagem_ia)




import io
import datetime as dt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Exemplo Streamlit – Formulário e Ações", page_icon="🧩", layout="wide")

# -------------------------------
# Estado inicial
# -------------------------------
if "envios" not in st.session_state:
    st.session_state.envios = []  # lista de dicionários
if "ultimo_upload" not in st.session_state:
    st.session_state.ultimo_upload = None

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.header("🔧 Configurações")
    modo = st.radio("Modo", ["Padrão", "Avançado"], horizontal=True)
    tema = st.selectbox("Tema visual", ["Claro", "Escuro", "Auto"])
    st.divider()
    st.markdown("Demonstração de uma sidebar com controles e descrição.")
    st.caption("Dica: clique em 'Limpar formulário' para resetar os campos.")

# -------------------------------
# Título/Descrição
# -------------------------------
st.title("🧩 Página com Streamlit – Campos e Botões")
st.write(
    "Este é um exemplo de página com formulário, validação, upload de arquivo, "
    "botões e estado de sessão. Adapte livremente para seu caso."
)

# -------------------------------
# Layout principal
# -------------------------------
col_form, col_info = st.columns([2, 1], gap="large")

with col_form:
    st.subheader("📋 Formulário de Cadastro")

    # Usando st.form para agrupar envio
    with st.form("form_cadastro", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome completo*", placeholder="Digite seu nome")
            email = st.text_input("E-mail*", placeholder="nome@empresa.com")
            data_nasc = st.date_input(
                "Data de nascimento",
                value=None,
                min_value=dt.date(1900,1,1),
                max_value=dt.date.today()
            )
            qtd = st.number_input("Quantidade", min_value=0, max_value=1000, value=1, step=1)

        with col2:
            cargo = st.selectbox("Cargo", ["", "Analista", "Especialista", "Coordenador", "Gerente", "Diretor"])
            habilidades = st.multiselect(
                "Habilidades",
                ["Python", "Streamlit", "Excel", "Power BI", "Automação", "SQL", "Git"],
                default=["Streamlit"] if modo == "Padrão" else []
            )
            ativo = st.checkbox("Ativo", value=True)
            prioridade = st.slider("Prioridade (0-10)", 0, 10, 5)

        obs = st.text_area("Observações", placeholder="Informações adicionais...")

        uploaded = st.file_uploader(
            "Upload opcional (CSV ou XLSX)",
            type=["csv", "xlsx"],
            accept_multiple_files=False
        )

        # Botões do formulário
        enviar = st.form_submit_button("🚀 Enviar", use_container_width=True)
        limpar = st.form_submit_button("🧹 Limpar formulário", use_container_width=True)

    # Lógica dos botões do formulário
    if enviar:
        erros = []
        if not nome.strip():
            erros.append("O campo **Nome completo** é obrigatório.")
        if not email.strip():
            erros.append("O campo **E-mail** é obrigatório.")
        elif "@" not in email or "." not in email.split("@")[-1]:
            erros.append("Informe um **E-mail** válido.")
        if cargo == "":
            erros.append("Selecione um **Cargo**.")

        if erros:
            for e in erros:
                st.error(e)
        else:
            registro = {
                "nome": nome.strip(),
                "email": email.strip(),
                "data_nasc": str(data_nasc) if data_nasc else None,
                "quantidade": int(qtd),
                "cargo": cargo,
                "habilidades": ", ".join(habilidades),
                "ativo": ativo,
                "prioridade": int(prioridade),
                "obs": obs.strip(),
                "data_envio": dt.datetime.now().isoformat(timespec="seconds"),
            }
            st.session_state.envios.append(registro)
            st.success("Dados enviados com sucesso! ✅")

            if uploaded is not None:
                try:
                    if uploaded.name.lower().endswith(".csv"):
                        df_up = pd.read_csv(uploaded)
                    else:
                        df_up = pd.read_excel(uploaded, engine="openpyxl")
                    st.session_state.ultimo_upload = df_up
                    st.info(f"Arquivo **{uploaded.name}** processado ({df_up.shape[0]} linhas x {df_up.shape[1]} colunas).")
                except Exception as ex:
                    st.warning(f"Não foi possível ler o arquivo: {ex}")

    if limpar:
        for k in list(st.session_state.keys()):
            # mantenha histórico e último upload; limpe só campos derivados
            if k not in ("envios", "ultimo_upload"):
                st.session_state[k] = st.session_state[k]
        st.experimental_rerun()

with col_info:
    st.subheader("ℹ️ Info")
    st.write("**Total de envios:**", len(st.session_state.envios))
    if st.session_state.envios:
        df_envios = pd.DataFrame(st.session_state.envios)
        st.dataframe(df_envios, use_container_width=True, height=220)

        # Exportar CSV em memória
        csv_buf = io.StringIO()
        df_envios.to_csv(csv_buf, index=False)
        st.download_button(
            "💾 Baixar envios (CSV)",
            data=csv_buf.getvalue().encode("utf-8"),
            file_name="envios.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.divider()
    st.subheader("📎 Último upload")
    if st.session_state.ultimo_upload is not None:
        st.dataframe(st.session_state.ultimo_upload, use_container_width=True, height=220)
    else:
        st.caption("Nenhum arquivo carregado ainda.")

# -------------------------------
# Ações fora do formulário
# -------------------------------
st.divider()
st.subheader("⚙️ Ações rápidas")

col_a, col_b, col_c = st.columns(3)
with col_a:
    if st.button("🔄 Processar último upload", use_container_width=True, type="secondary"):
        if st.session_state.ultimo_upload is None:
            st.warning("Nenhum arquivo foi carregado.")
        else:
            df = st.session_state.ultimo_upload.copy()
            # Exemplo de transformação simples
            df.columns = [c.strip().upper() for c in df.columns]
            st.session_state.ultimo_upload = df
            st.success("Último upload processado: colunas normalizadas (maiúsculas).")

with col_b:
    if st.button("🗑️ Limpar histórico de envios", use_container_width=True):
        st.session_state.envios = []
        st.success("Histórico limpo.")

with col_c:
    if st.button("📤 Exportar tudo (CSV)", use_container_width=True):
        df_all = pd.DataFrame(st.session_state.envios) if st.session_state.envios else pd.DataFrame()
        if df_all.empty:
            st.info("Não há envios para exportar.")
        else:
            buf = io.StringIO()
            df_all.to_csv(buf, index=False)
            st.download_button(
                "⬇️ Clique para baixar agora",
                data=buf.getvalue().encode("utf-8"),
                file_name=f"export_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="dl_export_inline"
            )

# Rodapé
st.markdown("---")
st.caption("Exemplo criado com ❤️ usando Streamlit. Adapte para seus fluxos de trabalho.")
