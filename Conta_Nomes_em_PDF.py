import os
import glob
import fitz
import re
import pandas as pd
import copy

# Função Específica: transforma em string o texto de um pdf grande
def buscar_legendas(pdf_path):
    legendas = []
    with fitz.open(pdf_path) as pdf_documento:
        for numero_pagina, pagina in enumerate(pdf_documento, start=1):
            texto_pagina = pagina.get_text("text").replace('\n', ' ')
            legendas.append((texto_pagina, numero_pagina))
    return legendas

    
# Função Independente: Pode ser usada em contextos diferentes
def divide_nomes_personagens(nomes_personagens):
    partes_dos_nomes = [nome.split() for nome in nomes_personagens]; cont = 0
    for line in partes_dos_nomes:
        line.append(nomes_personagens[cont])
        cont += 1
    return partes_dos_nomes

###############################################################################################

# Função Auxiliar --> p/ Função Principal "listar_posicoes_nomes_na_legenda"
def procura_nome_no_texto(nome, texto_pagina):
    # Compila a expressão regular para capturar o nome seguido por caracteres não-alfanuméricos
    pattern = re.compile(r'\b' + re.escape(nome) + r'\b\W*')
    lista_posicao = []
    for match in pattern.finditer(texto_pagina):
        # print(nome, match.group(), match.start())
        lista_posicao.append(match.start())
    return lista_posicao

# Detecta as posições dos nomes ao longo das páginas do texto
def listar_posicoes_nomes_na_legenda(legendas, partes_dos_nomes):
    lista_final_posicoes_nome = []
    for texto_pagina, numero_pagina in legendas:    
        lista_das_listas_de_personagens = []
        for line in partes_dos_nomes:
            lista_personagem = []
            for nome in line:
                lista_posicao = procura_nome_no_texto(nome, texto_pagina)
                lista_personagem.append([nome, lista_posicao])
            lista_das_listas_de_personagens.append([line[-1],lista_personagem])
        lista_final_posicoes_nome.append([numero_pagina, lista_das_listas_de_personagens])
    return lista_final_posicoes_nome

###############################################################################################

# Função Auxiliar --> p/ função principal "gera_lista_posicoes_final"
def elimina_repeticoes_entre_duas_lst_e_gera_tres_lst_finais(lst_a, lst_b, lst_c,tamanho_nome):
    # Criar listas finais iniciando como cópias das listas originais
    lst_a_final = lst_a[:]; lst_b_final = lst_b[:]; lst_c_final = lst_c[:]
    # Percorrer uma cópia da lst_a para evitar modificar a lista enquanto itera
    for a in lst_a[:]:
        for c in lst_c[:]:
            if a == c:
                lst_a_final.remove(a) # Remover o elemento de lst_a_final
    for b in lst_b[:]:
        for c in lst_c[:]:
            if (b-tamanho_nome) == c:
                lst_b_final.remove(b) # Remover o elemento de lst_b_final
    
    return lst_a_final, lst_b_final, lst_c_final

# Elimina_nomes_repetidos_da_lista_posicoes_bruto
# def gera_lista_posicoes_final(lista_posicoes_bruto):
#     lista_posicoes_bruto_final = copy.deepcopy(lista_posicoes_bruto)
    
#     for num_pag, lst_pag in lista_posicoes_bruto_final:
#         for personagem, lst_personagem in lst_pag:
            
#             lst_das_lst_posicoes_aux = []; tamanho_nomes = []
#             for nome, lst_posicoes in lst_personagem:
#                 lst_das_lst_posicoes_aux.append(lst_posicoes) 
#                 tamanho_nomes.append(len(nome)+1) # +1 pra add o caracter de espaço
                
#             lst_a, lst_b, lst_c = lst_das_lst_posicoes_aux
#             lst_a_final, lst_b_final, lst_c_final = elimina_repeticoes_entre_duas_lst_e_gera_tres_lst_finais(lst_a, lst_b, lst_c,tamanho_nomes[0])    
#             lst_das_lst_posicoes_aux_corrigida = [lst_a_final, lst_b_final, lst_c_final]
            
#             cont = 0
#             for i in range(len(lst_personagem)):
#                 lst_personagem[i] = (lst_personagem[i][0], lst_das_lst_posicoes_aux_corrigida[cont])
#                 cont += 1
                
#     return lista_posicoes_bruto_final

def gera_lista_posicoes_final(lista_posicoes_bruto):
    lista_posicoes_bruto_final = copy.deepcopy(lista_posicoes_bruto)
    
    for num_pag, lst_pag in lista_posicoes_bruto_final:
        for personagem, lst_personagem in lst_pag:
            
            lst_das_lst_posicoes_aux = []
            tamanho_nomes = []
            for nome, lst_posicoes in lst_personagem:
                lst_das_lst_posicoes_aux.append(lst_posicoes)
                tamanho_nomes.append(len(nome) + 1)  # +1 pra add o caracter de espaço
            
            # Garantir que lst_das_lst_posicoes_aux tem exatamente 3 elementos
            while len(lst_das_lst_posicoes_aux) < 3:
                lst_das_lst_posicoes_aux.append([])  # Adiciona listas vazias se necessário
            
            lst_a, lst_b, lst_c = lst_das_lst_posicoes_aux[:3]  # Considera apenas os três primeiros elementos
            lst_a_final, lst_b_final, lst_c_final = elimina_repeticoes_entre_duas_lst_e_gera_tres_lst_finais(lst_a, lst_b, lst_c, tamanho_nomes[0])    
            lst_das_lst_posicoes_aux_corrigida = [lst_a_final, lst_b_final, lst_c_final]
            
            cont = 0
            for i in range(len(lst_personagem)):
                lst_personagem[i] = (lst_personagem[i][0], lst_das_lst_posicoes_aux_corrigida[cont])
                cont += 1
                
    return lista_posicoes_bruto_final


###############################################################################################

# Serve para contar o número de posições que cada personagem têm por página (divido por nomes)
def gera_lista_contagem_por_pag_dos_nomes_na_lista_posicoes(lista_posicoes):
    lst_contagem_por_pag = []
    for pag, lst_personagens in lista_posicoes:
        lst_contagem_por_nome_completo = []
        for nome_completo, lst_nomes in lst_personagens:
            lst_contagem_nome = []
            for nome, lst_posicoes in lst_nomes:
                lst_contagem_nome.append([nome, len(lst_posicoes)])
            lst_contagem_por_nome_completo.append([nome_completo, lst_contagem_nome])                    
        lst_contagem_por_pag.append([pag, lst_contagem_por_nome_completo])
        
    return lst_contagem_por_pag

# Função Auxiliar para simplificar lista complexa do código
def simplifica_estrutura(lst_posicoes):
    lista_simplificada = []
    for grupo in lst_posicoes:
        numero_grupo = grupo[0]
        personagens = grupo[1]
        for personagem in personagens:
            nome = personagem[0]
            scores = [item[1] for item in personagem[1]]
            lista_simplificada.append([numero_grupo, nome] + scores)
    return lista_simplificada

# Conta o valor final das vezes que cada Personagem aparece no texto
# (somando todas as páginas e somando nome + sobrenome)
def conta_personagens(lst_posicoes_simplificada, nomes_personagens):
    dicionario_contagem = {}
    for nome in nomes_personagens:
        dicionario_contagem[nome] = 0
  
    for line in lst_posicoes_simplificada:
        soma = line[-1] + line[-2] + line[-3] 
        dicionario_contagem[line[1]] = dicionario_contagem[line[1]] + soma

    return dicionario_contagem

# Conta o valor final das vezes que cada Nome, Sobrenome e Nome Completo do Personagem aparece no texto
# (somando todas as páginas e totalizando valores diferentes para nome, sobrenome e nome completo)
def conta_personagens_nome_sobrenome(lst_posicoes_simplificada, nomes_personagens):
    dicionario_contagem = {}
    for nome in nomes_personagens:
        dicionario_contagem[nome] = [0,0,0]
  
    for line in lst_posicoes_simplificada:
        dicionario_contagem[line[1]][0] = dicionario_contagem[line[1]][0] + line[-3]
        dicionario_contagem[line[1]][1] = dicionario_contagem[line[1]][1] + line[-2]
        dicionario_contagem[line[1]][2] = dicionario_contagem[line[1]][2] + line[-1]

    return dicionario_contagem
    
##############################################################################################


def gerar_df_padrao_timeline_histograma(lst_contagem_nomes_final_simplificada, nomes_personagens):
    personagens = {nome: {} for nome in nomes_personagens}
    for item in lst_contagem_nomes_final_simplificada:
        pagina, personagem, *valores = item
        if personagem in personagens:
            soma = sum(valores[-3:])  # Somente as três últimas colunas
            personagens[personagem][pagina] = personagens[personagem].get(pagina, 0) + soma
        else:
            print(f"Nome desconhecido encontrado: {personagem}")
    
    # Cria DataFrame a partir do dicionário de personagens
    df_personagens = pd.DataFrame.from_dict(personagens, orient='index').sort_index(axis=1)
    
    return df_personagens    

##############################################################################################

def gerar_df_padrao_timeline_histograma(lst_contagem_nomes_final_simplificada, nomes_personagens):
    personagens = {nome: {} for nome in nomes_personagens}
    for item in lst_contagem_nomes_final_simplificada:
        pagina, personagem, *valores = item
        if personagem in personagens:
            soma = sum(valores[-3:])  # Somente as três últimas colunas
            personagens[personagem][pagina] = personagens[personagem].get(pagina, 0) + soma
        else:
            print(f"Nome desconhecido encontrado: {personagem}")
    
    # Cria DataFrame a partir do dicionário de personagens
    df_personagens = pd.DataFrame.from_dict(personagens, orient='index').sort_index(axis=1)
    
    # Aplica soma acumulada ao longo das colunas
    df_personagens = df_personagens.cumsum(axis=1)
    
    return df_personagens

def gerar_df_padrao_timeline_histograma(lst_contagem_nomes_final_simplificada, nomes_personagens):
    personagens = {nome: {} for nome in nomes_personagens}
    for item in lst_contagem_nomes_final_simplificada:
        pagina, personagem, *valores = item
        if personagem in personagens:
            soma = sum(valores[-3:])  # Somente as três últimas colunas
            personagens[personagem][pagina] = personagens[personagem].get(pagina, 0) + soma
        else:
            print(f"Nome desconhecido encontrado: {personagem}")
    
    # Cria DataFrame a partir do dicionário de personagens
    df_personagens = pd.DataFrame.from_dict(personagens, orient='index').sort_index(axis=1)
    
    # Aplica soma acumulada ao longo das colunas
    df_personagens = df_personagens.cumsum(axis=1)
    
    return df_personagens

##############################################################################################

def Conta_Nomes_em_pdf(nomes_personagens, pdf_path, nome_arquivo_csv):
    print("Iniciando a contagem de nomes...")  # Debug
    partes_dos_nomes = divide_nomes_personagens(nomes_personagens)
    
    # Usando o caminho do PDF específico
    legendas = buscar_legendas(pdf_path)
    
    lista_posicoes_bruto = listar_posicoes_nomes_na_legenda(legendas, partes_dos_nomes)
    lista_posicoes_final = gera_lista_posicoes_final(lista_posicoes_bruto)
    lst_contagem_nomes_final = gera_lista_contagem_por_pag_dos_nomes_na_lista_posicoes(lista_posicoes_final)
    lst_contagem_nomes_final_simplificada = simplifica_estrutura(lst_contagem_nomes_final)

    df_contagem_timeline_histograma = gerar_df_padrao_timeline_histograma(lst_contagem_nomes_final_simplificada, nomes_personagens)
    
    if not df_contagem_timeline_histograma.empty:
        df_contagem_timeline_histograma.to_csv(nome_arquivo_csv, index=True)
        print(f"DataFrame salvo como {nome_arquivo_csv}")
    else:
        print("DataFrame está vazio. Nenhum nome foi contado.")


