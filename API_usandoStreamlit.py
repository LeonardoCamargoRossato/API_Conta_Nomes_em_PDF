import streamlit as st
from Conta_Nomes_em_PDF import Conta_Nomes_em_pdf
import pandas as pd
import tempfile

# Variável para o tamanho da fonte do título
titulo_tamanho_fonte = "32px"  # Você pode ajustar este valor para alterar o tamanho da fonte

# Título da aplicação com tamanho de fonte personalizável usando HTML
st.markdown(f'<h1 style="font-size: {titulo_tamanho_fonte};">API: Contando Nomes/Palavras em PDF</h1>', unsafe_allow_html=True)

# Upload do arquivo PDF
pdf_file = st.file_uploader("Selecione o PDF:", type=["pdf"], key="pdf_uploader")

# Campos para entrada de dados
nomes_personagens = st.text_area(
    "Nomes dos Personagens (separados por vírgula):",
    placeholder="Exemplo: Harry Potter, Hermione, Rony Weasley, Alvo"
)
nome_arquivo_csv = st.text_input("Nome do Arquivo CSV:", placeholder="Exemplo: resultados.csv")

# Botão de processamento
if st.button("Processar"):
    if pdf_file is not None and nomes_personagens and nome_arquivo_csv:
        # Adicionar extensão .csv se não estiver presente
        if not nome_arquivo_csv.endswith('.csv'):
            nome_arquivo_csv += '.csv'

        # Definir o caminho completo para salvar o arquivo CSV gerado
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_csv:
            caminho_arquivo_csv = temp_csv.name

        # Processar os nomes dos personagens e remover espaços em branco extras
        nomes_personagens_lista = [nome.strip() for nome in nomes_personagens.split(',') if nome.strip()]
        
        # Verificação de entrada: Exibir os nomes processados
        st.write("Nomes dos Personagens (processados):", nomes_personagens_lista)

        # Verificar se há nomes válidos para processar
        if nomes_personagens_lista:
            # Processamento do PDF diretamente do objeto do arquivo
            st.write("Iniciando processamento do PDF...")
            
            # Salvar o PDF temporariamente em um caminho em memória
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(pdf_file.getbuffer())
                temp_pdf_path = temp_pdf.name
            
            # Chamar a função de contagem de nomes usando o caminho temporário
            Conta_Nomes_em_pdf(nomes_personagens_lista, temp_pdf_path, caminho_arquivo_csv)

            # Verificar o conteúdo do arquivo CSV após a criação
            df = pd.read_csv(caminho_arquivo_csv)
            st.write("Conteúdo do CSV Gerado:", df)

            # Cria um botão para download do arquivo CSV gerado
            with open(caminho_arquivo_csv, "rb") as file:
                btn = st.download_button(
                    label="Download do arquivo CSV",
                    data=file,
                    file_name=nome_arquivo_csv,
                    mime="text/csv"
                )

            # Exibir mensagem de sucesso
            st.success(f"O arquivo {nome_arquivo_csv} foi gerado com sucesso!")
        else:
            st.error("Nenhum nome de personagem válido foi fornecido. Por favor, insira nomes separados por vírgula.")
    else:
        st.error("Por favor, carregue um PDF e insira os nomes dos personagens e o nome do arquivo CSV.")

