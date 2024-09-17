import streamlit as st
from Conta_Nomes_em_PDF import Conta_Nomes_em_pdf
import os

# Configurações iniciais
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Cria o diretório se não existir

STATIC_FOLDER = 'static'
os.makedirs(STATIC_FOLDER, exist_ok=True)  # Cria o diretório se não existir

# Título da aplicação
st.title('Upload PDF e Processamento')

# Upload do arquivo PDF
pdf_file = st.file_uploader("Selecione o PDF:", type=["pdf"], key="pdf_uploader")

# Campos para entrada de dados
nomes_personagens = st.text_area("Nomes dos Personagens (separados por vírgula):", 
                                 placeholder="Exemplo: Harry Potter, Hermione Granger, Ron Weasley")
nome_arquivo_csv = st.text_input("Nome do Arquivo CSV:", placeholder="Exemplo: resultados.csv")

# Botão de processamento
if st.button("Processar"):
    if pdf_file is not None and nomes_personagens and nome_arquivo_csv:
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.name)
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.getbuffer())

        if not nome_arquivo_csv.endswith('.csv'):
            nome_arquivo_csv += '.csv'

        caminho_arquivo_csv = os.path.join(STATIC_FOLDER, nome_arquivo_csv)
        nomes_personagens_lista = nomes_personagens.split(',')

        # Processamento do PDF
        Conta_Nomes_em_pdf(nomes_personagens_lista, pdf_path, caminho_arquivo_csv)

        # Cria um botão para download do arquivo CSV
        with open(caminho_arquivo_csv, "rb") as file:
            btn = st.download_button(
                label="Download do arquivo CSV",
                data=file,
                file_name=nome_arquivo_csv,
                mime="text/csv"
            )

