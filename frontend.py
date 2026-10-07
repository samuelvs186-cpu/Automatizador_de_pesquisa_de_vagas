import requests
import streamlit as st


st.set_page_config(
    page_title="Central de Vagas", 
    page_icon="💼", 
    layout="centered"
)


st.title("💼 Central de Vagas e Oportunidades")
st.write("Digite a tecnologia para ativar a busca automática via Playwright e FastAPI.")


API_URL = "http://localhost:8000"


with st.form("busca_form"):
    termo = st.text_input("Tecnologia ou Cargo (ex: Python, Data Analyst, DevOps):")
    submeter = st.form_submit_button("Buscar Vagas")

if submeter and termo:
    with st.spinner("Buscando vagas..."):
        try:
            resposta = requests.post(f"{API_URL}/vagas/buscar", json={"termo": termo})
            if resposta.status_code == 200:
                st.success("Vagas encontradas e salvas com sucesso!")
            else:
                st.error("Erro ao buscar vagas no servidor.")
        except Exception as err:
            st.error(f"Erro ao conectar com a API: {err}")



st.subheader("🗒️ Painel de Vagas Cadastradas")

try:
    resposta = requests.get(f"{API_URL}/vagas")
    
    if resposta.status_code == 200:
        vagas = resposta.json()
        
        if not vagas:
            st.info("Nenhuma vaga cadastrada ainda. Faça uma busca para adicionar vagas.")
        else:
            for vaga in vagas:
                with st.container():
                    st.markdown(f"### {vaga['titulo']}")
                    st.caption(f"Empresa: **{vaga['empresa']}**")
                    st.markdown(f"[👉 Clique aqui para se candidatar]({vaga['link']})")
                    st.divider()
    else:
        st.error("Erro ao carregar a lista de vagas do servidor.")

except Exception:
    st.warning("Não foi possível conectar com a API para listar as vagas. Verifique se a API está rodando.")
