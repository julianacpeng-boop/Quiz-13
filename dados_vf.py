"""Uma afirmação por vídeo para o formato Juh Quiz Verdadeiro ou Falso."""

PERGUNTAS = [
    {
        "pergunta": "A lenda do lobisomem foi inventada pelo cinema moderno?",
        "verdadeiro": False,
        "explicacao": (
            "Histórias de lobisomens já circulavam no mundo antigo. "
            "A mitologia e o folclore greco-romanos registravam narrativas "
            "de transformação entre pessoas e lobos muito antes do cinema."
        ),
        "imagem": "imagens_perguntas/lobisomem.png",
        "legenda": "Será que a lenda do lobisomem nasceu no cinema? Descubra neste desafio!",
        "hashtags": ['#Lobisomem', '#Folclore', '#Mitologia', '#JuhQuiz'],
    },
    {
        "pergunta": "A crença em bruxas surgiu somente na Idade Média?",
        "verdadeiro": False,
        "explicacao": (
            "Ideias sobre magia e figuras chamadas de bruxas aparecem em fontes "
            "da Antiguidade. A imagem da bruxa mudou ao longo do tempo e não "
            "tem uma única origem."
        ),
        "imagem": "imagens_perguntas/bruxa.png",
        "legenda": "A história das bruxas é muito mais antiga do que você imagina. Acerte esse verdadeiro ou falso!",
        "hashtags": ['#Bruxas', '#História', '#Mistérios', '#JuhQuiz'],
    },
    {
        "pergunta": "A lenda dos vampiros começou com o livro Drácula?",
        "verdadeiro": False,
        "explicacao": (
            "Relatos e crenças populares sobre mortos que voltariam à vida "
            "existiam na Europa antes do romance Drácula, publicado em 1897. "
            "A literatura ajudou a moldar a imagem moderna do vampiro."
        ),
        "imagem": "imagens_perguntas/vampiro.png",
        "legenda": "Drácula foi mesmo o começo das histórias de vampiros? Teste seus conhecimentos!",
        "hashtags": ['#Vampiros', '#Drácula', '#Folclore', '#JuhQuiz'],
    },
    {
        "pergunta": "Plínio, o Jovem, contou uma história de casa assombrada na Roma antiga?",
        "verdadeiro": True,
        "explicacao": (
            "Em uma carta escrita no século I, Plínio descreveu uma casa em "
            "Atenas onde se ouvia o som de correntes e aparecia o fantasma "
            "de um homem."
        ),
        "imagem": "imagens_perguntas/fantasma.png",
        "legenda": "Uma das histórias de casa assombrada mais antigas tem quase 2 mil anos. Verdade ou mentira?",
        "hashtags": ['#Fantasma', '#História', '#Mistérios', '#JuhQuiz'],
    },
    {
        "pergunta": "A figura do zumbi do folclore haitiano tem raízes ligadas à história do Haiti e a crenças populares?",
        "verdadeiro": True,
        "explicacao": (
            "A tradição haitiana do zumbi se desenvolveu em um contexto "
            "histórico marcado pela escravidão e se relaciona a crenças "
            "populares associadas ao Vodou. O zumbi de filmes ganhou outras "
            "características."
        ),
        "imagem": "imagens_perguntas/zumbi.png",
        "legenda": "Você conhece as raízes do zumbi no folclore haitiano? Descubra neste desafio!",
        "hashtags": ['#Zumbi', '#FolcloreHaitiano', '#Cultura', '#JuhQuiz'],
    },
    {
        "pergunta": "Dragões aparecem em mitologias antigas de diferentes culturas?",
        "verdadeiro": True,
        "explicacao": (
            "Sim. Seres parecidos com dragões ou grandes serpentes aparecem "
            "em tradições antigas de várias regiões, como Mesopotâmia, Egito, "
            "Grécia, China e outras culturas."
        ),
        "imagem": "imagens_perguntas/dragao.png",
        "legenda": "Dragões aparecem em histórias antigas de várias culturas. Você sabia?",
        "hashtags": ['#Dragões', '#Mitologia', '#Curiosidades', '#JuhQuiz'],
    },
    {
        "pergunta": "No Egito antigo, apenas faraós podiam ser mumificados?",
        "verdadeiro": False,
        "explicacao": (
            "Não. A mumificação foi praticada em pessoas de diferentes grupos e também em animais. "
            "O tipo de preparação variava conforme o período, as crenças e os recursos disponíveis."
        ),
        "imagem": "imagens_perguntas/mumia.png",
        "legenda": "Só os faraós eram mumificados? Essa história tem mais camadas do que uma múmia!",
        "hashtags": ['#Múmias', '#EgitoAntigo', '#História', '#JuhQuiz'],
    },
    {
        "pergunta": "No romance de Mary Shelley, Frankenstein é o nome da criatura?",
        "verdadeiro": False,
        "explicacao": (
            "Frankenstein é o sobrenome de Victor, o cientista que cria a criatura. "
            "No romance original, o ser não recebe um nome próprio; a cultura popular acabou misturando os dois."
        ),
        "imagem": "imagens_perguntas/frankenstein.png",
        "legenda": "Chamamos a criatura pelo nome errado? Descubra neste quiz arrepiante!",
        "hashtags": ['#Frankenstein', '#Literatura', '#Terror', '#JuhQuiz'],
    },
    {
        "pergunta": "Na mitologia grega, Medusa era uma das três Górgonas?",
        "verdadeiro": True,
        "explicacao": (
            "Sim. Medusa fazia parte do trio das Górgonas. Em muitas representações conhecidas, "
            "ela aparece com serpentes no cabelo e um olhar capaz de transformar pessoas em pedra."
        ),
        "imagem": "imagens_perguntas/medusa.png",
        "legenda": "Medusa tinha mesmo duas irmãs Górgonas? Cuidado com o olhar e responda!",
        "hashtags": ['#Medusa', '#MitologiaGrega', '#Lendas', '#JuhQuiz'],
    },
    {
        "pergunta": "Na tradição irlandesa, o lamento da banshee podia anunciar uma morte na família?",
        "verdadeiro": True,
        "explicacao": (
            "Sim. Segundo o folclore irlandês, o grito ou lamento da banshee era associado ao aviso "
            "da morte de alguém ligado à família. É uma crença tradicional, não um fato comprovado."
        ),
        "imagem": "imagens_perguntas/banshee.png",
        "legenda": "Esse grito sobrenatural era um aviso? Conheça a lenda irlandesa da banshee!",
        "hashtags": ['#Banshee', '#FolcloreIrlandês', '#Lendas', '#JuhQuiz'],
    },
    {
        "pergunta": "O Cavaleiro sem Cabeça ficou famoso no conto de Washington Irving, publicado em 1820?",
        "verdadeiro": True,
        "explicacao": (
            "Sim. A história de Washington Irving, publicada em 1820, ajudou a popularizar a perseguição "
            "sobrenatural do Cavaleiro sem Cabeça em Sleepy Hollow. O personagem depois ganhou muitas versões."
        ),
        "imagem": "imagens_perguntas/cavaleiro_sem_cabeca.png",
        "legenda": "O Cavaleiro sem Cabeça surgiu em um conto de 1820. Você sabia dessa?",
        "hashtags": ['#CavaleiroSemCabeça', '#SleepyHollow', '#Literatura', '#JuhQuiz'],
    },
    {
        "pergunta": "As primeiras lanternas da tradição do Jack-o’-lantern eram feitas de abóboras?",
        "verdadeiro": False,
        "explicacao": (
            "Não. Na tradição irlandesa, eram usados nabos escavados com uma brasa dentro. "
            "A abóbora se tornou comum depois que a tradição chegou aos Estados Unidos."
        ),
        "imagem": "imagens_perguntas/lanterna_nabo.png",
        "legenda": "A primeira lanterna assustadora era de nabo, não de abóbora!",
        "hashtags": ['#JackOLantern', '#Halloween', '#Folclore', '#JuhQuiz'],
    },
]
