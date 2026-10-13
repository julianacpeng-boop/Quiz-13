# Juh Quiz — Quiz-13 Verdadeiro ou Falso

O Quiz-13 gera um vídeo vertical por afirmação, com a identidade visual aprovada e a mesma voz usada no Quiz-10.

## Como fica o vídeo

- Formato vertical 1080 × 1920 (9:16).
- A faixa superior mostra “Verdadeiro ou Falso?”, a marca discreta “Juh Quiz” e o tema.
- A afirmação e a caricatura ficam juntas na mesma caixa clara. A ilustração mantém a proporção e aparece maior, sem uma caixa colorida atrás.
- Verdadeiro e Falso aparecem lado a lado durante a pergunta.
- Depois da leitura e da contagem de 3 segundos, o botão errado some. A resposta correta fica sozinha no primeiro espaço e muda para verde (Verdadeiro) ou vermelho (Falso).
- A explicação é digitada no espaço abaixo enquanto a narração fala.
- As quatro paletas vibrantes mudam a cada três vídeos: verde, azul, vermelho e roxo. Ao passar pela quarta, o ciclo recomeça.
- Perguntas e explicações usam ajuste automático de fonte e altura. Se o texto ultrapassar o limite de leitura, o gerador interrompe com uma mensagem clara antes de salvar um vídeo cortado.
- O TXT começa com `CAPA_SEGUNDOS=2` e inclui legenda e hashtags.

## Voz

Usa `pt-BR-AntonioNeural` com velocidade `+10%`, seguindo o padrão de conexão do Quiz-10. O gerador tenta novamente quando o serviço falha e, se ainda assim não responder, usa a voz local em português para concluir a execução. A voz Edge não exige uma chave Azure.

## Pastas

```text
gerar_vf.py
dados_vf.py
requirements-vf.txt
FONTES.md
imagens_perguntas/
.github/workflows/gerar-vf.yml
```

As caricaturas incluídas têm 970 × 970 px. Para novas imagens, use PNG, JPG, JPEG ou WebP e mantenha-as dentro de `imagens_perguntas/`. O programa preserva a proporção e adapta a área da imagem ao espaço que sobrar depois da afirmação.

## Cadastrar pergunta, legenda e imagem

Edite somente `dados_vf.py` para adicionar ou alterar uma pergunta. Informe `tema` para o selo no topo (opcional; sem ele, o programa usa o nome do arquivo de imagem). `imagem` pode ser `None`.

```python
{
    "tema": "LOBO-GUARÁ",
    "pergunta": "O lobo-guará é um lobo?",
    "verdadeiro": False,
    "explicacao": "Apesar do nome, o lobo-guará pertence a um gênero próprio e não é um lobo verdadeiro.",
    "imagem": "imagens_perguntas/lobisomem.png",
    "legenda": "O lobo-guará é mesmo um lobo? Responda antes da revelação!",
    "hashtags": ["#LoboGuará", "#Animais", "#Curiosidades", "#JuhQuiz"],
}
```

Use `True` para verdadeiro e `False` para falso. As perguntas são montadas em sequência; cada bloco de três usa a mesma paleta.

## Google Drive e GitHub Actions

1. No repositório Quiz-13, abra **Settings → Secrets and variables → Actions**.
2. Crie o secret `RCLONE_DRIVE_TOKEN` e cole o JSON completo do token rclone que você usa no Quiz-10.
3. Abra **Actions → Quiz-13 — Verdadeiro ou Falso → Run workflow**.
4. A execução salva MP4 e TXT no Drive em `saida/Juh-Quiz-13/verdadeiro-ou-falso/execucao-ID/` e publica uma cópia para baixar como artefato do Actions.

O workflow usa a pasta-base já configurada nos projetos anteriores e não depende de salvar a chave neste arquivo ou em `dados_vf.py`. Quem cadastra perguntas só precisa editar `dados_vf.py` e colocar as imagens na pasta indicada.

## Gerar localmente

Instale Python 3.11, FFmpeg e os pacotes abaixo. Para envio local ao Drive, instale e configure também o rclone.

```bash
python -m pip install -r requirements-vf.txt
python gerar_vf.py
```

Para enviar ao Drive pela execução local, configure as variáveis do rclone e execute `python gerar_vf.py --enviar-drive`.
