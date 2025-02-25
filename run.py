import streamlit as st
from docx import Document
import io
# Configuração da página do Streamlit
st.set_page_config(page_title="Modelos de Petições", page_icon="📝")

def preencher_contrato(razao, nome, cnpj, endereco, cidade_estadio, valor, data, modelo_contrato):
    # Carrega o documento do Word
    doc = Document(modelo_contrato)

    # Itera sobre todos os parágrafos do documento
    for paragraph in doc.paragraphs:
        paragraph.text = paragraph.text.replace('{{RAZAO}}', razao)
        paragraph.text = paragraph.text.replace('{{NOME}}', nome)
        paragraph.text = paragraph.text.replace('{{CNPJ}}', cnpj)
        paragraph.text = paragraph.text.replace('{{ENDERECO}}', endereco)
        paragraph.text = paragraph.text.replace('{{CIDADE/ESTADO}}', cidade_estadio)
        paragraph.text = paragraph.text.replace('{{VALOR}}', valor)
        paragraph.text = paragraph.text.replace('{{DATA}}', data)

    # Salva o documento em um buffer de memória
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Título da aplicação
st.title("Gerador de Petições")

# Lista de modelos de contrato
modelos = {
    "Petição modelo 1": r"Documento sem título.docx",
    "Petição modelo 2": r"Documento sem título2.docx"
}

# Inicializa o estado da sessão para armazenar os valores dos campos e controle de download
if 'razao' not in st.session_state:
    st.session_state.razao = ""
if 'nome' not in st.session_state:
    st.session_state.nome = ""
if 'cnpj' not in st.session_state:
    st.session_state.cnpj = ""
if 'endereco' not in st.session_state:
    st.session_state.endereco = ""
if 'cidade_estadio' not in st.session_state:
    st.session_state.cidade_estadio = ""
if 'valor' not in st.session_state:
    st.session_state.valor = ""
if 'data' not in st.session_state:
    st.session_state.data = ""
if 'contrato_preenchido' not in st.session_state:
    st.session_state.contrato_preenchido = None  # Armazena o contrato gerado

# Selecionar o tipo de contrato
tipo_contrato = st.selectbox("Selecione o tipo de petição:", list(modelos.keys()))

# Campos de entrada
st.session_state.razao = st.text_input("Razão:", value=st.session_state.razao)
st.session_state.nome = st.text_input("Nome:", value=st.session_state.nome)
st.session_state.cnpj = st.text_input("CNPJ:", value=st.session_state.cnpj)
st.session_state.endereco = st.text_input("Endereço:", value=st.session_state.endereco)
st.session_state.cidade_estadio = st.text_input("Cidade/Estado:", value=st.session_state.cidade_estadio)
st.session_state.valor = st.text_input("Valor:", value=st.session_state.valor)
st.session_state.data = st.text_input("Data:", value=st.session_state.data)

# Botão para gerar o contrato
if st.button("Gerar Contrato"):
    if st.session_state.nome and st.session_state.cnpj and st.session_state.endereco:
        modelo_selecionado = modelos[tipo_contrato]
        st.session_state.contrato_preenchido = preencher_contrato(
            st.session_state.razao, st.session_state.nome, st.session_state.cnpj,
            st.session_state.endereco, st.session_state.cidade_estadio,
            st.session_state.valor, st.session_state.data, modelo_selecionado
        )
        st.success("Contrato gerado com sucesso! Agora você pode baixá-lo.")
    else:
        st.error("Por favor, preencha todos os campos.")

# Botão de download só aparece se o contrato foi gerado
if st.session_state.contrato_preenchido:
    st.download_button(
        label="Baixar Contrato",
        data=st.session_state.contrato_preenchido,
        file_name=f"contrato_{tipo_contrato.replace(' ', '_').lower()}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    
    # Limpa os campos após o download
    for campo in ["razao", "nome", "cnpj", "endereco", "cidade_estadio", "valor", "data", "contrato_preenchido"]:
        st.session_state[campo] = ""
