"""Doze vídeos verdadeiros ou falsos para o Juh Quiz — Quiz-13."""

PERGUNTAS = [
    {
        "tema": "TRIÂNGULO DAS BERMUDAS",
        "pergunta": "O Triângulo das Bermudas é uma região oficial com limites definidos pela NOAA?",
        "verdadeiro": False,
        "explicacao": (
            "Não. A NOAA informa que não há mapas oficiais que definam os limites do chamado Triângulo das Bermudas. "
            "O nome ficou popular por causa de relatos e histórias sobre a região."
        ),
        "imagem": "imagens_perguntas/triangulo_bermudas.png",
        "legenda": "O Triângulo das Bermudas tem mesmo fronteiras oficiais? Responda antes da revelação!",
        "hashtags": ["#TriânguloDasBermudas", "#Mistério", "#Curiosidades", "#JuhQuiz"],
    },
    {
        "tema": "MONSTRO DO LAGO NESS",
        "pergunta": "A fotografia mais famosa do monstro do Lago Ness foi revelada como uma fraude?",
        "verdadeiro": True,
        "explicacao": (
            "Sim. A famosa foto de 1934, conhecida como fotografia do cirurgião, foi posteriormente revelada como uma fraude. "
            "Mesmo assim, ela ajudou a espalhar a lenda de Nessie."
        ),
        "imagem": "imagens_perguntas/lago_ness.png",
        "legenda": "A foto mais famosa de Nessie enganou o mundo? Descubra neste verdadeiro ou falso!",
        "hashtags": ["#LagoNess", "#Nessie", "#Mistérios", "#JuhQuiz"],
    },
    {
        "tema": "ATLÂNTIDA",
        "pergunta": "A história conhecida de Atlântida aparece em textos do filósofo Platão?",
        "verdadeiro": True,
        "explicacao": (
            "Sim. Platão contou a história de Atlântida nos diálogos Timeu e Crítias. "
            "A narrativa é antiga, mas isso não comprova que a cidade perdida tenha existido de verdade."
        ),
        "imagem": "imagens_perguntas/atlantida.png",
        "legenda": "Atlântida apareceu primeiro em textos antigos de Platão. Você sabia?",
        "hashtags": ["#Atlântida", "#Platão", "#História", "#JuhQuiz"],
    },
    {
        "tema": "MURALHA DA CHINA",
        "pergunta": "É possível ver a Grande Muralha da China a olho nu da Lua?",
        "verdadeiro": False,
        "explicacao": (
            "Não. A NASA explica que a Muralha não pode ser vista da Lua a olho nu. "
            "Até da órbita baixa da Terra, ela é difícil de enxergar sem lentes potentes."
        ),
        "imagem": None,
        "legenda": "A Muralha da China aparece mesmo da Lua? Teste esse mito famoso!",
        "hashtags": ["#MuralhaDaChina", "#Espaço", "#Curiosidades", "#JuhQuiz"],
    },
    {
        "tema": "CÉREBRO HUMANO",
        "pergunta": "Usamos apenas 10% do nosso cérebro?",
        "verdadeiro": False,
        "explicacao": (
            "Não. Essa porcentagem é um neuromito. Diferentes áreas do cérebro participam de funções variadas, "
            "e exames mostram atividade cerebral distribuída, não limitada a apenas 10%."
        ),
        "imagem": None,
        "legenda": "Será que usamos só 10% do cérebro? A resposta pode surpreender!",
        "hashtags": ["#Cérebro", "#Ciência", "#Mitos", "#JuhQuiz"],
    },
    {
        "tema": "MORCEGOS",
        "pergunta": "Os morcegos são cegos?",
        "verdadeiro": False,
        "explicacao": (
            "Não. Morcegos têm visão. Muitas espécies também usam a ecolocalização: emitem sons e percebem o eco "
            "para se orientar e encontrar alimento no escuro."
        ),
        "imagem": None,
        "legenda": "Morcegos enxergam ou vivem só pelo sonar? Descubra!",
        "hashtags": ["#Morcegos", "#Animais", "#Ciência", "#JuhQuiz"],
    },
    {
        "tema": "KRAKEN",
        "pergunta": "O Kraken faz parte do folclore escandinavo como um monstro marinho?",
        "verdadeiro": True,
        "explicacao": (
            "Sim. O Kraken é um monstro marinho lendário ligado ao folclore escandinavo. "
            "Descrições antigas podem ter sido inspiradas por animais reais, como lulas gigantes, mas o Kraken lendário não é um animal comprovado."
        ),
        "imagem": "imagens_perguntas/kraken.png",
        "legenda": "O Kraken nasceu como lenda dos mares do norte. Você encararia esse monstro?",
        "hashtags": ["#Kraken", "#Folclore", "#MonstrosMarinhos", "#JuhQuiz"],
    },
    {
        "tema": "CHUPACABRA",
        "pergunta": "Os relatos modernos do Chupacabra começaram em Porto Rico nos anos 1990?",
        "verdadeiro": True,
        "explicacao": (
            "Sim. A onda de relatos que popularizou o Chupacabra começou em Porto Rico em 1995. "
            "A criatura pertence ao folclore moderno e suas descrições variam."
        ),
        "imagem": "imagens_perguntas/chupacabra.png",
        "legenda": "O Chupacabra surgiu nas histórias modernas de Porto Rico. Verdade ou lenda?",
        "hashtags": ["#Chupacabra", "#Folclore", "#Mistérios", "#JuhQuiz"],
    },
    {
        "tema": "MOTHMAN",
        "pergunta": "Os primeiros relatos famosos do Mothman surgiram em Point Pleasant em 1966?",
        "verdadeiro": True,
        "explicacao": (
            "Sim. Relatos de uma criatura alada e de olhos brilhantes foram publicados perto de Point Pleasant, "
            "na Virgínia Ocidental, em novembro de 1966. O Mothman faz parte do folclore local."
        ),
        "imagem": "imagens_perguntas/mothman.png",
        "legenda": "A lenda do Mothman começou em 1966? Veja a resposta neste desafio!",
        "hashtags": ["#Mothman", "#Lendas", "#Mistério", "#JuhQuiz"],
    },
    {
        "tema": "PLANETAS",
        "pergunta": "Mercúrio é o planeta mais quente do Sistema Solar?",
        "verdadeiro": False,
        "explicacao": (
            "Não. Embora esteja mais perto do Sol, Mercúrio não é o mais quente. "
            "Vênus tem uma atmosfera muito densa que retém calor e deixa sua superfície ainda mais quente."
        ),
        "imagem": None,
        "legenda": "Mercúrio é o planeta mais quente só por estar mais perto do Sol?",
        "hashtags": ["#SistemaSolar", "#Planetas", "#Astronomia", "#JuhQuiz"],
    },
    {
        "tema": "RAIOS",
        "pergunta": "Um raio nunca cai duas vezes no mesmo lugar?",
        "verdadeiro": False,
        "explicacao": (
            "Falso. Raios podem atingir o mesmo local várias vezes, especialmente estruturas altas, pontudas e isoladas. "
            "A ideia de que isso nunca acontece é apenas um ditado popular."
        ),
        "imagem": None,
        "legenda": "O raio nunca cai duas vezes no mesmo lugar? Responda antes do trovão!",
        "hashtags": ["#Raios", "#Clima", "#Curiosidades", "#JuhQuiz"],
    },
    {
        "tema": "POLVOS",
        "pergunta": "Os polvos têm três corações?",
        "verdadeiro": True,
        "explicacao": (
            "Sim. Dois corações bombeiam sangue pelas brânquias e um terceiro envia o sangue para o resto do corpo. "
            "A natureza realmente caprichou nesse animal!"
        ),
        "imagem": None,
        "legenda": "Três corações? O polvo é mais surpreendente do que parece!",
        "hashtags": ["#Polvo", "#VidaMarinha", "#Curiosidades", "#JuhQuiz"],
    },
]
