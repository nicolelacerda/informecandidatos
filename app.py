from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import textwrap
import openai
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
token_openai=os.environ.get("TOKEN_OPENAI")


def raspador_noticias(palavras_chave):
    site_url = "https://www1.folha.uol.com.br/folha-topicos/eleicoes-2024/"
    resposta = requests.get(site_url)
    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, 'html.parser')
        noticias = soup.find_all('div', {"class": "c-headline c-headline--newslist"})
        dict_noticias = {palavra_chave: [] for palavra_chave in palavras_chave}
        noticias_por_candidato = {palavra_chave: 0 for palavra_chave in palavras_chave}
        for noticia in noticias:
            if all(noticias_por_candidato[palavra_chave] >= 5 for palavra_chave in palavras_chave):
                break  #sair do loop ao encontrar 5 notícias para cada candidato
            titulo = noticia.find('a').text.strip()
            link = noticia.find('a')['href']
            for palavra_chave in palavras_chave:
                if palavra_chave.lower() in noticia.text.lower():
                    if noticias_por_candidato[palavra_chave] < 5:
                        texto = texto_completo(link)
                        dict_noticias[palavra_chave].append({'titulo': titulo, 'link': link, 'texto': texto})
                        noticias_por_candidato[palavra_chave] += 1
    return dict_noticias

def texto_completo(link):
    resposta = requests.get(link)
    if resposta.status_code == 200: 
        soup = BeautifulSoup(resposta.text, 'html.parser') 
        texto = soup.find('div', {"class": 'c-news__body'})
        if texto:
            texto_formatado = texto.text.strip().replace('\n', '\n\n')
            largura_da_tela = 150
            texto_final = textwrap.fill(texto_formatado, width=largura_da_tela)
            return texto_final
        
def resumo_materia(texto_completo):
    prompt = "Sou uma jornalista e estou fazendo uma newsletter com notícias sobre três candidatos para a prefeitura de São Paulo nas eleições de 2024. Estou te apresentando uma função que extrai notícias agrupadas por palavras-chave. Cada palavra-chave leva o nome de um candidato. Para cada candidato (palavra-chave) foram extraídas 5 notícias. Quero que você faça um resumo de no máximo 300 caracteres sobre cada notícia. Siga os seguintes passos: 1- Leia as notícias extraídas na função. 2 - Separe trechos importantes que podem ser essenciais para o eleitor se informar sobre o candidato. 3 - Faça um resumo de no máximo 300 caracteres sobre a notícia. 4 - É obrigatório que o resumo tenha o nome do candidato sugerido na palavra-chave. 5 - O resumo pode ter alguma aspa importante, mas não é obrigatório. 6 - Preciso que os resumos referentes a cada notícia estejam separados com espaçamento."
    openai_api_key = token_openai
    client = openai.Client(api_key = openai_api_key)
    response = client.chat.completions.create(
            model="gpt-4-1106-preview", 
            messages=[
                        {"role": "user", "content": prompt},
                        {"role": "user", "content": texto_completo}
                  ]
    )
    if response.choices:
        resumo = response.choices[0].message.content 
        largura_da_tela = 150
        resumo_formatado = textwrap.fill(resumo, width=largura_da_tela)
        return resumo_formatado 

@app.route("/paginainicial", methods=["GET", "POST"])
def paginainicial():
    if request.method == "POST": 
        palavras_chave = ["Nunes", "Boulos", "Tabata"]
        noticias_por_candidato = raspador_noticias(palavras_chave)
        return render_template("paginainicial.html", noticias_por_candidato=noticias_por_candidato)
    else:
        return render_template("paginainicial.html")

# Rota para página do candidato 1
@app.route("/guilhermeboulos")
def candidato1():
    palavras_chave = ["Boulos"]
    noticias_por_candidato = raspador_noticias(palavras_chave)
    resumos = []
    for noticia in noticias_por_candidato['Boulos']:
        titulo = noticia['titulo']
        texto = noticia['texto']
        resumo = resumo_materia(texto)
        resumos.append({'titulo': titulo, 'resumo': resumo})
    return render_template("guilhermeboulos.html", resumos=resumos)

# Rota para página do candidato 2
@app.route("/ricardonunes")
def candidato2():
    palavras_chave = ["Nunes"]
    noticias_por_candidato = raspador_noticias(palavras_chave)
    resumos = []
    for noticia in noticias_por_candidato['Nunes']:
        titulo = noticia['titulo']
        texto = noticia['texto']
        resumo = resumo_materia(texto)
        resumos.append({'titulo': titulo, 'resumo': resumo})
    return render_template("ricardonunes.html", resumos=resumos)


# Rota para página do candidato 3
@app.route("/tabataamaral")
def candidato3():
    palavras_chave = ["Tabata"]
    noticias_por_candidato = raspador_noticias(palavras_chave)
    resumos = []
    for noticia in noticias_por_candidato['Tabata']:
        titulo = noticia['titulo']
        texto = noticia['texto']
        resumo = resumo_materia(texto)
        resumos.append({'titulo': titulo, 'resumo': resumo})
    return render_template("tabataamaral.html", resumos=resumos)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
