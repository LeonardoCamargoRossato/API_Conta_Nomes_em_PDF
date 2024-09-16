from flask import Flask, request, render_template, redirect, url_for
from Conta_Nomes_em_PDF import Conta_Nomes_em_pdf  # Importação da função do arquivo externo
import os

app = Flask(__name__)

# Diretório onde os PDFs enviados serão salvos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Cria o diretório se não existir
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Diretório onde os arquivos gerados (CSV) serão salvos
STATIC_FOLDER = 'static'
os.makedirs(STATIC_FOLDER, exist_ok=True)  # Cria o diretório se não existir

# Página inicial com o formulário para upload do PDF e inputs para a função Conta_Nomes_em_pdf
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Lida com o upload do PDF
        pdf_file = request.files['pdf']
        if pdf_file:
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(pdf_path)

            # Captura os inputs do usuário
            nomes_personagens = request.form.get('nomes_personagens').split(',')
            nome_arquivo_csv = request.form.get('nome_arquivo_csv')

            # Adiciona extensão .csv ao nome do arquivo, se necessário
            if not nome_arquivo_csv.endswith('.csv'):
                nome_arquivo_csv += '.csv'

            # Define o caminho completo onde o CSV será salvo
            caminho_arquivo_csv = os.path.join(STATIC_FOLDER, nome_arquivo_csv)

            # Chama a função Conta_Nomes_em_pdf com o caminho completo para salvar o CSV
            Conta_Nomes_em_pdf(nomes_personagens, caminho_arquivo_csv)

            # Redireciona para a página de download do arquivo CSV gerado
            return redirect(url_for('download', filename=nome_arquivo_csv))

    # Renderiza a página inicial com o formulário
    return render_template('index.html')

# Página para baixar o CSV gerado
@app.route('/download/<filename>')
def download(filename):
    # Redireciona para a pasta 'static' para fazer o download do arquivo especificado
    return redirect(url_for('static', filename=filename))

# Executa o aplicativo se o script for executado diretamente
if __name__ == '__main__':
    app.run(debug=True)

