
import io
import datetime as dt
import pandas as pd
import streamlit as st

# =====================================================
# CONFIGURAÇÃO DA PÁGINA (APENAS UMA VEZ)
# =====================================================
st.set_page_config(
    page_title="Exemplo Streamlit – Formulário e Ações",
    page_icon="🧩",
    layout="wide"
)

# =====================================================
# LOGIN SIMPLES (BLOQUEIA TODO O APP)
# =====================================================
USUARIO_CORRETO = "Admin"
SENHA_CORRETA = "Admin"

if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("🔐 Acesso restrito")

    with st.form("login_form"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar")

    if entrar:
        if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
            st.session_state.logado = True
            st.success("Login realizado com sucesso ✅")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos ❌")

    # ⛔ Impede qualquer código abaixo de rodar
    st.stop()

# =====================================================
# ESTADO INICIAL
# =====================================================
if "envios" not in st.session_state:
    st.session_state.envios = []
if "ultimo_upload" not in st.session_state:
    st.session_state.ultimo_upload = None

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.header("🔧 Configurações")

    if st.button("🔓 Logout"):
        st.session_state.logado = False
        st.rerun()

    modo = st.radio("Modo", ["Padrão", "Avançado"], horizontal=True)
    tema = st.selectbox("Tema visual", ["Claro", "Escuro", "Auto"])

    st.divider()
    st.caption("Dica: clique em 'Limpar formulário' para resetar os campos.")

# =====================================================
# TÍTULO / DESCRIÇÃO
# =====================================================
st.title("🧩 Desenvolvido por Juliano Mitsutake")
st.write(
    "Formulário com validação, upload de arquivos, controle de sessão "
    "e ações rápidas. Adapte livremente para seu trabalho."
)

# =====================================================
# LAYOUT PRINCIPAL
# =====================================================
col_form, col_info = st.columns([2, 1], gap="large")

# =====================================================
# FORMULÁRIO
# =====================================================
with col_form:
    st.subheader("📋 Formulário de Cadastro")

    with st.form("form_cadastro"):
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome completo*")
            email = st.text_input("E-mail*")
            data_nasc = st.date_input(
                "Data de nascimento",
                value=None,
                min_value=dt.date(1900, 1, 1),
                max_value=dt.date.today()
            )
            qtd = st.number_input("Quantidade", min_value=0, max_value=1000, value=1)

        with col2:
            cargo = st.selectbox(
                "Cargo",
                ["", "Analista", "Especialista", "Coordenador", "Gerente", "Diretor"]
            )
            habilidades = st.multiselect(
                "Habilidades",
                ["Python", "Streamlit", "Excel", "Power BI",
                 "Automação", "SQL", "Git"],
                default=["Streamlit"] if modo == "Padrão" else []
            )
            ativo = st.checkbox("Ativo", value=True)
            prioridade = st.slider("Prioridade (0-10)", 0, 10, 5)

        obs = st.text_area("Observações")

        uploaded = st.file_uploader(
            "Upload opcional (CSV ou XLSX)",
            type=["csv", "xlsx"]
        )

        enviar = st.form_submit_button("🚀 Enviar")
        limpar = st.form_submit_button("🧹 Limpar formulário")

    if enviar:
        erros = []
        if not nome.strip():
            erros.append("O campo **Nome completo** é obrigatório.")
        if not email.strip():
            erros.append("O campo **E-mail** é obrigatório.")
        elif "@" not in email:
            erros.append("Informe um **e-mail válido**.")
        if cargo == "":
            erros.append("Selecione um **Cargo**.")

        if erros:
            for e in erros:
                st.error(e)
        else:
            registro = {
                "nome": nome,
                "email": email,
                "data_nasc": str(data_nasc) if data_nasc else None,
                "quantidade": int(qtd),
                "cargo": cargo,
                "habilidades": ", ".join(habilidades),
                "ativo": ativo,
                "prioridade": int(prioridade),
                "obs": obs,
                "data_envio": dt.datetime.now().isoformat(timespec="seconds"),
            }
            st.session_state.envios.append(registro)
            st.success("Dados enviados com sucesso ✅")

            if uploaded:
                try:
                    if uploaded.name.lower().endswith(".csv"):
                        df = pd.read_csv(uploaded)
                    else:
                        df = pd.read_excel(uploaded, engine="openpyxl")
                    st.session_state.ultimo_upload = df
                    st.info(f"Arquivo **{uploaded.name}** carregado com sucesso.")
                except Exception as e:
                    st.error(f"Erro ao ler arquivo: {e}")

    if limpar:
        st.rerun()

# =====================================================
# PAINEL DE INFORMAÇÕES
# =====================================================
with col_info:
    st.subheader("ℹ️ Informações")
    st.write("Total de envios:", len(st.session_state.envios))

    if st.session_state.envios:
        df_envios = pd.DataFrame(st.session_state.envios)
        st.dataframe(df_envios, use_container_width=True, height=250)

        csv_buf = io.StringIO()
        df_envios.to_csv(csv_buf, index=False)

        st.download_button(
            "💾 Baixar envios (CSV)",
            data=csv_buf.getvalue().encode("utf-8"),
            file_name="envios.csv",
            mime="text/csv"
        )

    st.divider()
    st.subheader("📎 Último upload")
    if st.session_state.ultimo_upload is not None:
        st.dataframe(st.session_state.ultimo_upload, use_container_width=True, height=220)
    else:
        st.caption("Nenhum arquivo carregado ainda.")

# =====================================================
# AÇÕES RÁPIDAS
# =====================================================
st.divider()
st.subheader("⚙️ Ações rápidas")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🔄 Processar último upload"):
        if st.session_state.ultimo_upload is None:
            st.warning("Nenhum arquivo foi carregado.")
        else:
            df = st.session_state.ultimo_upload.copy()
            df.columns = [c.strip().upper() for c in df.columns]
            st.session_state.ultimo_upload = df
            st.success("Colunas normalizadas com sucesso.")

with c2:
    if st.button("🗑️ Limpar histórico"):
        st.session_state.envios = []
        st.success("Histórico de envios limpo.")

with c3:
    if st.button("📤 Exportar tudo"):
        if not st.session_state.envios:
            st.info("Não há dados para exportar.")
        else:
            df_all = pd.DataFrame(st.session_state.envios)
            buf = io.StringIO()
            df_all.to_csv(buf, index=False)
            st.download_button(
                "⬇️ Baixar agora",
                data=buf.getvalue().encode("utf-8"),
                file_name=f"export_{dt.datetime.now():%Y%m%d_%H%M%S}.csv",
                mime="text/csv"
            )

# =====================================================
# RODAPÉ
# =====================================================
st.markdown("---")
st.caption("Aplicação Streamlit protegida por login simples.")
