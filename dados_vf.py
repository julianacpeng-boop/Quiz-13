"""Quiz-13: 15 afirmações; uma caricatura com fundo por vídeo.
O gerador existente escreve CAPA_SEGUNDOS=2 no TXT automaticamente.
"""

PERGUNTAS = [
    {
        "tema": "Halloween",
        "pergunta": "O Halloween também é conhecido como Dia das Bruxas.",
        "verdadeiro": True,
        "explicacao": "No Brasil, Dia das Bruxas é o nome popular dado ao Halloween.",
        "imagem": "imagens_perguntas/01_halloween.png",
        "legenda": "Você conhece essa festa cheia de fantasias e mistérios? Verdadeiro ou falso?",
        "hashtags": [
            "#Halloween",
            "#DiaDasBruxas",
            "#Curiosidades",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Desgramou — Felipe Araújo",
        "pergunta": "A música “Desgramou” é interpretada por Felipe Araújo.",
        "verdadeiro": True,
        "explicacao": "Felipe Araújo é o intérprete de Desgramou, divulgada na campanha musical mostrada no Kwai.",
        "imagem": "imagens_perguntas/02_desgramou.png",
        "legenda": "Quem acompanha o sertanejo vai acertar? Dê seu palpite antes da resposta!",
        "hashtags": [
            "#Desgramou",
            "#FelipeAraujo",
            "#Sertanejo",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Willow e a Floresta Encantada",
        "pergunta": "Em “Willow e a Floresta Encantada”, a floresta está ameaçada pelo desmatamento.",
        "verdadeiro": True,
        "explicacao": "Na história apresentada na divulgação do filme, Willow precisa ajudar a proteger a floresta ameaçada pelo desmatamento.",
        "imagem": "imagens_perguntas/03_willow.png",
        "legenda": "Uma floresta, muita magia e um desafio! Você conhece a história de Willow?",
        "hashtags": [
            "#Willow",
            "#FlorestaEncantada",
            "#Cinema",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Votação até as 19h",
        "pergunta": "A prorrogação da votação até as 19h autorizou a reabertura de urnas que já estavam encerradas.",
        "verdadeiro": False,
        "explicacao": "No segundo turno de 2026, a extensão valia apenas para os locais onde a votação ainda não havia sido encerrada às 17h.",
        "imagem": "imagens_perguntas/04_eleicoes_19h.png",
        "legenda": "Votação até as 19h: a decisão permitia reabrir urnas encerradas? Confira o esclarecimento do TSE.",
        "hashtags": [
            "#Eleicoes2026",
            "#Votacao",
            "#FatoOuFake",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Corpo humano",
        "pergunta": "O coração humano possui quatro cavidades.",
        "verdadeiro": True,
        "explicacao": "O coração humano tem dois átrios e dois ventrículos, totalizando quatro cavidades.",
        "imagem": "imagens_perguntas/05_coracao.png",
        "legenda": "Você conhece bem o órgão que bate sem parar? Verdadeiro ou falso?",
        "hashtags": [
            "#Coracao",
            "#CorpoHumano",
            "#Ciencia",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Animais surpreendentes",
        "pergunta": "Os polvos possuem três corações.",
        "verdadeiro": True,
        "explicacao": "Dois corações bombeiam sangue para as brânquias e outro o envia para o restante do corpo.",
        "imagem": "imagens_perguntas/06_polvo.png",
        "legenda": "Esse morador dos oceanos guarda uma surpresa! Acerte antes da revelação.",
        "hashtags": [
            "#Polvo",
            "#Animais",
            "#Curiosidades",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Origem das comidas",
        "pergunta": "O sushi é um prato tradicional da culinária chinesa.",
        "verdadeiro": False,
        "explicacao": "O sushi, na forma pela qual é conhecido atualmente, é um prato tradicional da culinária japonesa.",
        "imagem": "imagens_perguntas/07_sushi.png",
        "legenda": "Você sabe de qual culinária esse prato faz parte? Responda verdadeiro ou falso!",
        "hashtags": [
            "#Sushi",
            "#Gastronomia",
            "#Cultura",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Língua portuguesa",
        "pergunta": "“Mas” e “mais” podem ser usados com o mesmo significado.",
        "verdadeiro": False,
        "explicacao": "Mas normalmente indica oposição. Mais expressa quantidade ou intensidade; as duas palavras não são intercambiáveis.",
        "imagem": "imagens_perguntas/08_portugues.png",
        "legenda": "Uma letra muda tudo! Você domina essa pegadinha da língua portuguesa?",
        "hashtags": [
            "#Portugues",
            "#Gramatica",
            "#Aprendizado",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Descontos e matemática",
        "pergunta": "Um desconto de 50% seguido de outro de 50% torna o produto gratuito.",
        "verdadeiro": False,
        "explicacao": "O segundo desconto incide sobre o valor já reduzido. Um produto de 100 reais passa a custar 25 reais.",
        "imagem": "imagens_perguntas/09_descontos.png",
        "legenda": "Dois descontos de 50%: quanto sobra para pagar? Pense antes de responder!",
        "hashtags": [
            "#Matematica",
            "#Descontos",
            "#Desafio",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Segredos do espaço",
        "pergunta": "Vênus é o planeta mais quente do Sistema Solar.",
        "verdadeiro": True,
        "explicacao": "Sua atmosfera densa, rica em dióxido de carbono, retém muito calor por meio de um intenso efeito estufa.",
        "imagem": "imagens_perguntas/10_venus.png",
        "legenda": "Qual planeta ganha no calor? Teste seus conhecimentos sobre o Sistema Solar.",
        "hashtags": [
            "#Venus",
            "#Espaco",
            "#Astronomia",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Invenções",
        "pergunta": "O telefone foi inventado antes da internet.",
        "verdadeiro": True,
        "explicacao": "O telefone surgiu no século XIX. As redes que deram origem à internet apareceram no século XX.",
        "imagem": "imagens_perguntas/11_invencoes.png",
        "legenda": "Telefone ou internet: você conhece a ordem dessas invenções? Verdadeiro ou falso?",
        "hashtags": [
            "#Invencoes",
            "#Tecnologia",
            "#Historia",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Notícias na internet",
        "pergunta": "Uma notícia muito compartilhada na internet é sempre verdadeira.",
        "verdadeiro": False,
        "explicacao": "O número de compartilhamentos não comprova uma notícia. É preciso verificar fonte, data e evidências.",
        "imagem": "imagens_perguntas/12_noticias.png",
        "legenda": "Milhares de compartilhamentos significam que é verdade? Confira esse desafio.",
        "hashtags": [
            "#Internet",
            "#Noticias",
            "#FatoOuFake",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Geografia do Brasil",
        "pergunta": "O Brasil faz fronteira com todos os países da América do Sul.",
        "verdadeiro": False,
        "explicacao": "Chile e Equador são os dois países sul-americanos que não fazem fronteira com o Brasil.",
        "imagem": "imagens_perguntas/13_brasil.png",
        "legenda": "Você conhece os vizinhos do Brasil? Acerte essa de geografia!",
        "hashtags": [
            "#Brasil",
            "#Geografia",
            "#AmericaDoSul",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Símbolos",
        "pergunta": "A pomba branca é um símbolo de paz.",
        "verdadeiro": True,
        "explicacao": "A pomba branca é amplamente utilizada como símbolo de paz em manifestações culturais e artísticas.",
        "imagem": "imagens_perguntas/14_pomba.png",
        "legenda": "Você reconhece o significado desse símbolo? Dê seu palpite!",
        "hashtags": [
            "#Paz",
            "#Simbolos",
            "#Curiosidades",
            "#JuhQuiz"
        ]
    },
    {
        "tema": "Procurando Nemo",
        "pergunta": "No filme “Procurando Nemo”, Nemo é um peixe-palhaço.",
        "verdadeiro": True,
        "explicacao": "Nemo e seu pai, Marlin, são peixes-palhaço, conhecidos pelas cores alaranjadas e faixas brancas.",
        "imagem": "imagens_perguntas/15_nemo.png",
        "legenda": "Quem se lembra dessa aventura no fundo do mar? Verdadeiro ou falso?",
        "hashtags": [
            "#ProcurandoNemo",
            "#Cinema",
            "#Animacao",
            "#JuhQuiz"
        ]
    }
]

