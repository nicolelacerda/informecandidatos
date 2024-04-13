# informecandidatos
Trabalho feito para a disciplina de Projeto do 3º trimestre para o Master em Jornalismo de Dados, Automação e Data Storytelling, do Insper. 

## Objetivo
Construir uma newsletter, que será atualizada diariamente com um resumo dos assuntos envolvendo cada candidato à prefeitura de SP que foram publicados em sites de notícias ao longo do dia. Objetivo é fazer com que o leitor consiga ter um panorama rápido sobre o dia do candidato sem precisar acessar vários portais.

## Bibliotecas

> Flask
Criar o site na web

> gunicorn
Implantar o flask na web

> requests
Fazer solicitações HTTP

> bs4
Scraping

> textwrap
Formatar o texto

> openai
Gerar resumos automáticos 

>python-dotenv
Usar variáveis de ambiente


## app.py
Código de um site que extrai notícias sobre três candidatos à prefeitura de São Paulo nas eleições de 2024 (Guilherme Boulos, Ricardo Nunes e Tabata Amaral), faz resumos das notícias raspadas e exibe esses resumos em páginas HTML separadas para cada candidato.

> A função raspador_noticias busca na aba da editoria de política e eleições do jornal Folha de São Paulo as notícias que tenham os termos "Boulos" , "Nunes" e "Tabata" no título.

> A função texto_completo entra no link da notícia selecionada na função acima e extrai o texto_completo da matéria.

> A função resumo_materia pega os textos completos da função anterior e utiliza a API da OpenAI para gerar resumo automáticos de casda notícia.


## Rotas páginas HTML

> Função /paginainicial:
É a página inicial do site, possui um formulário com os nomes dos candidatos. O usuário deve selecionar um dos candidatos e será redirecionado para a página com o resumo das notícias referente o candidato escolhido. 

> Funções: candidato1 (/guilhermeboulos), candidato2 (/ricardonunes), candidato3 (/tabataamaral):
Objetivo é renderizar as páginas de cada candidato. Extraem as notícias para o candidato usando a função raspador_noticias, resumem essas notícias chamando resumo_materia, e depois renderizam um modelo HTML para cada candidato,devolvendo os resumos das notícias.


