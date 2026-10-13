"""Gera vídeos Juh Quiz: uma afirmação V/F, pausa de 3 s e explicação."""

from __future__ import annotations

import asyncio
import argparse
import json
import math
import os
import re
import shutil
import subprocess
import tempfile
import unicodedata
import wave
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from PIL import Image, ImageDraw, ImageFont, ImageOps

from dados_vf import PERGUNTAS


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "saida_vf"
VOICE = "pt-BR-AntonioNeural"
RATE = "+10%"
VIDEO_W, VIDEO_H = 1080, 1920
IMAGE_BOX = (55, 500, 1025, 1470)  # left, top, right, bottom: 970 x 970 px
ANSWER_IMAGE_BOX = (55, 235, 1025, 1205)  # same 970 x 970 px on the answer screen
IMAGE_INSET = 50  # caricature appears 870 x 870 px inside the fixed 970 x 970 px frame
FPS = 30
DRIVE_BASE = "DESTINO:saida/Juh-Quiz-13/verdadeiro-ou-falso"
PALETTES = [
    {"name": "VERDE ELÉTRICO", "bg": ((10, 72, 50), (12, 116, 74)), "band": (10, 93, 62), "band2": (255, 196, 40), "accent": "#ffd84d", "card": "#f8f4e9", "ink": "#17251f", "muted": "#e5f5eb", "line": "#ffc42d"},
    {"name": "AZUL IMPACTO", "bg": ((8, 42, 113), (13, 93, 167)), "band": (8, 45, 128), "band2": (0, 205, 224), "accent": "#35d7df", "card": "#fff9e9", "ink": "#14253a", "muted": "#e0f4ff", "line": "#35d7df"},
    {"name": "VERMELHO SHOW", "bg": ((113, 20, 36), (180, 37, 47)), "band": (137, 17, 36), "band2": (255, 171, 31), "accent": "#ffb52e", "card": "#fff5e8", "ink": "#32151b", "muted": "#ffe9dc", "line": "#ffb52e"},
    {"name": "ROXO DIVERTIDO", "bg": ((71, 20, 111), (128, 23, 139)), "band": (79, 19, 122), "band2": (255, 191, 0), "accent": "#ffc43d", "card": "#fff8e9", "ink": "#2a1635", "muted": "#f4e4ff", "line": "#ffc43d"},
]
TRUE = "#18b844"
FALSE = "#ed2929"
CREAM = "#fff9ed"


def run(command: list[str]) -> None:
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL)


def require_program(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"Não encontrei {name}. Instale o FFmpeg e tente novamente.")
    return path


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and draw.textlength(candidate, font=font) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    font: ImageFont.ImageFont,
    fill: str,
    width: int,
    line_gap: int = 16,
    max_lines: int | None = None,
) -> int:
    x, y = xy
    lines = wrap_lines(draw, text, font, width)
    if max_lines and len(lines) > max_lines:
        raise ValueError(
            f"Texto longo demais para a tela ({len(lines)} linhas; máximo {max_lines}): {text}"
        )
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: str, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_height(lines: list[str], font: ImageFont.ImageFont, gap: int) -> int:
    return len(lines) * font.size + max(0, len(lines) - 1) * gap


def fit_text(draw: ImageDraw.ImageDraw, text: str, width: int, height: int,
             sizes=range(42, 19, -2), gap: int = 8) -> tuple[ImageFont.ImageFont, list[str]]:
    """Choose a readable font that fits; never clip text at the bottom of a card."""
    for size in sizes:
        font = load_font(size, True)
        lines = wrap_lines(draw, text, font, width)
        if text_height(lines, font, gap) <= height:
            return font, lines
    raise ValueError(f"Texto não cabe nem com fonte 20 px: {text[:90]}")


def make_paper(palette: dict) -> Image.Image:
    """Vibrant gradient canvas; palette changes every three videos."""
    strip = Image.new("RGB", (1, VIDEO_H))
    pixels = []
    for y in range(VIDEO_H):
        t = y / max(1, VIDEO_H - 1)
        pixels.append(tuple(round(palette["bg"][0][c] * (1 - t) + palette["bg"][1][c] * t) for c in range(3)))
    strip.putdata(pixels)
    canvas = strip.resize((VIDEO_W, VIDEO_H))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, VIDEO_W, 265), fill=palette["band"])
    draw.rectangle((0, 246, VIDEO_W, 264), fill=palette["band2"])
    return canvas


def paste_optional_image(
    canvas: Image.Image,
    image_path: Path | None,
    box: tuple[int, int, int, int],
) -> None:
    # Imagem é realmente opcional: sem arquivo, não desenhe moldura nem placeholder.
    if image_path is None:
        return
    left, top, right, bottom = box
    box_w, box_h = right - left, bottom - top
    draw = ImageDraw.Draw(canvas)
    inner_w, inner_h = box_w, box_h
    if not image_path.exists():
        raise FileNotFoundError(f"Imagem não encontrada: {image_path.relative_to(ROOT)}")
    with Image.open(image_path) as source:
        source = ImageOps.exif_transpose(source).convert("RGBA")
        # Keep the whole illustration visible; long questions give the image less height.
        fitted = ImageOps.contain(source, (inner_w, inner_h), method=Image.Resampling.LANCZOS)
        mask = Image.new("L", fitted.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, fitted.width - 1, fitted.height - 1), radius=28, fill=255)
        px = left + (box_w - fitted.width) // 2
        py = top + (box_h - fitted.height) // 2
        canvas.paste(fitted, (px, py), mask)


def draw_header(canvas: Image.Image, question: dict, palette: dict, response: bool = False) -> None:
    draw = ImageDraw.Draw(canvas)
    title = "VERDADEIRO OU FALSO"
    title_font = load_font(31, True)
    bounds = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((VIDEO_W - bounds[2] + bounds[0]) / 2, 66 - bounds[1]), title, font=title_font, fill=CREAM,
              stroke_width=2, stroke_fill="#171321")
    brand_font = load_font(46, True)
    brand_bounds = draw.textbbox((0, 0), "Juh Quiz", font=brand_font)
    draw.text((55, 142), "Juh Quiz", font=brand_font, fill=palette["accent"], stroke_width=1, stroke_fill="#21162c")
    fallback_theme = Path(str(question.get("imagem") or "DESAFIO DE HOJE")).stem.replace("_", " ")
    label = "RESPOSTA" if response else question.get("tema", fallback_theme).upper()
    pill = (55, 205, 600, 250)
    rounded(draw, pill, 18, palette["band2"])
    f, _ = fit_text(draw, label, 505, 34, range(24, 14, -1), 0)
    text_width = draw.textlength(label, font=f)
    draw.text((pill[0] + max(16, (pill[2] - pill[0] - text_width) / 2), 213), label, font=f, fill="#20182b")


def render_question_frame(question: dict, image_path: Path | None, palette: dict,
                          countdown: int | None = None) -> Image.Image:
    canvas = make_paper(palette)
    draw_header(canvas, question, palette)
    draw = ImageDraw.Draw(canvas)
    qfont, qlines = fit_text(draw, question["pergunta"], 880, 585, range(48, 19, -2), 8)
    y = 360
    for line in qlines:
        y += qfont.size + 8
    if image_path is not None:
        card_bottom = 1325
        image_top = max(560, y + 16)
        if 1295 - image_top < 320:
            raise ValueError("A pergunta é longa demais: reduza o texto para manter a imagem legível.")
        image_box = (95, image_top, 985, 1295)
        button_top = (1370, 1515)
    else:
        # Sem imagem, a caixa termina logo após a afirmação e as opções sobem.
        card_bottom = max(565, y + 48)
        button_top = (card_bottom + 45, card_bottom + 180)
    rounded(draw, (55, 285, 1025, card_bottom), 36, palette["card"], "#241a2b", 4)
    draw.text((95, 315), "A AFIRMAÇÃO É:", font=load_font(27, True), fill=palette["line"])
    y = 360
    for line in qlines:
        draw.text((95, y), line, font=qfont, fill=palette["ink"])
        y += qfont.size + 8
    if image_path is not None:
        paste_optional_image(canvas, image_path, image_box)
    draw = ImageDraw.Draw(canvas)
    buttons = ((95, button_top[0], 985, button_top[0] + 110, "VERDADEIRO"),
               (95, button_top[1], 985, button_top[1] + 110, "FALSO"))
    for box, label in ((b[:4], b[4]) for b in buttons):
        rounded(draw, (box[0], box[1] + 8, box[2], box[3] + 8), 30, "#17121b")
        rounded(draw, box, 30, palette["card"], "#241a2b", 4)
        f = load_font(52, True)
        tw = draw.textlength(label, font=f)
        draw.text(((VIDEO_W - tw) / 2, box[1] + 20), label, font=f, fill=palette["ink"])
    draw.text((295, 1680), "VOCÊ TEM 3 SEGUNDOS", font=load_font(27, True), fill=palette["muted"])
    if countdown is not None and image_path is not None:
        circle = (438, 700, 642, 904)
        draw.ellipse(circle, fill=palette["accent"], outline=CREAM, width=7)
        label = str(countdown)
        font = load_font(126, True)
        b = draw.textbbox((0, 0), label, font=font)
        center_x, center_y = (circle[0] + circle[2]) / 2, (circle[1] + circle[3]) / 2
        draw.text((center_x - (b[2] - b[0]) / 2 - b[0], center_y - (b[3] - b[1]) / 2 - b[1]), label,
                  font=font, fill=palette["ink"])
    return canvas


def render_answer_frame(question: dict, image_path: Path | None, palette: dict,
                        explanation_visible: str, base_canvas: Image.Image | None = None,
                        full_explanation: str | None = None) -> Image.Image:
    if base_canvas is None:
        canvas = render_question_frame(question, image_path, palette)
        draw = ImageDraw.Draw(canvas)
        # Replace both options with the correct one and a roomy explanation card.
        label = "VERDADEIRO" if question["verdadeiro"] else "FALSO"
        color = TRUE if question["verdadeiro"] else FALSE
        if image_path is not None:
            answer_top = 1370
            explanation_top, explanation_bottom = 1505, 1810
            clear_area = (82, 1350, 998, 1830)
            text_top, text_bottom = 1565, 1780
        else:
            qdraw = ImageDraw.Draw(canvas)
            qfont, qlines = fit_text(qdraw, question["pergunta"], 880, 585, range(48, 19, -2), 8)
            question_bottom = max(565, 360 + len(qlines) * (qfont.size + 8) + 48)
            answer_top = question_bottom + 45
            explanation_top = answer_top + 125
            text_top = explanation_top + 70
            full_text = full_explanation or explanation_visible or " "
            text_font, text_lines = fit_text(draw, full_text, 820, 800, range(36, 23, -1), 5)
            explanation_bottom = min(1810, max(explanation_top + 230,
                                               text_top + text_height(text_lines, text_font, 5) + 35))
            text_bottom = explanation_bottom - 25
            clear_area = (82, answer_top - 20, 998, 1830)
        draw.rectangle(clear_area, fill=palette["bg"][1])
        rounded(draw, (95, answer_top, 985, answer_top + 110), 30, color, "#21161f", 4)
        f = load_font(52, True)
        tw = draw.textlength(label, font=f)
        draw.text(((VIDEO_W - tw) / 2, answer_top + 20), label, font=f, fill="#ffffff", stroke_width=1, stroke_fill="#201820")
        rounded(draw, (95, explanation_top, 985, explanation_bottom), 26, palette["card"], "#241a2b", 3)
        draw.text((125, explanation_top + 24), "POR QUÊ?", font=load_font(24, True), fill=palette["line"])
        draw.text((420, 1840), "JUH QUIZ", font=load_font(24, True), fill=palette["muted"])
        base_canvas = canvas
    canvas = base_canvas.copy()
    draw = ImageDraw.Draw(canvas)
    # The explanation types into the space where the second option was.
    available = 820
    no_image = image_path is None
    full_text = full_explanation or explanation_visible or " "
    if no_image:
        qdraw = ImageDraw.Draw(canvas)
        qfont, qlines = fit_text(qdraw, question["pergunta"], 880, 585, range(48, 19, -2), 8)
        question_bottom = max(565, 360 + len(qlines) * (qfont.size + 8) + 48)
        explanation_top = question_bottom + 45 + 125
        text_top = explanation_top + 70
        text_font, text_lines = fit_text(draw, full_text, available, 800, range(36, 23, -1), 5)
        explanation_bottom = min(1810, max(explanation_top + 230,
                                           text_top + text_height(text_lines, text_font, 5) + 35))
        text_bottom = explanation_bottom - 25
    else:
        text_top, text_bottom = 1565, 1780
    text_height_available = max(100, text_bottom - text_top)
    font, _ = fit_text(draw, full_text, available, text_height_available,
                       range(36, 23, -1) if no_image else range(36, 18, -1), 5)
    lines = wrap_lines(draw, explanation_visible or " ", font, available)
    y = text_top
    for line in lines:
        draw.text((125, y), line, font=font, fill=palette["ink"])
        y += font.size + 5
    return canvas


def write_beep(path: Path, frequency: int = 950, seconds: float = 1.0) -> None:
    sample_rate = 48000
    total = int(sample_rate * seconds)
    beep_len = int(sample_rate * 0.12)
    with wave.open(str(path), "wb") as output:
        output.setnchannels(2)
        output.setsampwidth(2)
        output.setframerate(sample_rate)
        frames = bytearray()
        for i in range(total):
            if i < beep_len:
                fade = min(1.0, i / (sample_rate * 0.008), (beep_len - i) / (sample_rate * 0.025))
                value = int(7000 * fade * math.sin(2 * math.pi * frequency * i / sample_rate))
            else:
                value = 0
            frames.extend(value.to_bytes(2, "little", signed=True) * 2)
        output.writeframes(frames)


_EDGE_CONFIGURED = False


def configure_edge() -> None:
    """Use the Edge Services endpoint and current Edge browser headers."""
    global _EDGE_CONFIGURED
    import edge_tts.constants as constants
    import edge_tts.communicate as communicate
    import edge_tts.voices as voices

    version = os.getenv("QUIZ_EDGE_VERSION", "").strip()
    if version and not re.fullmatch(r"\d+\.\d+\.\d+\.\d+", version):
        raise ValueError("QUIZ_EDGE_VERSION precisa ser uma versão completa do Edge.")
    if not version:
        try:
            with urlopen("https://edgeupdates.microsoft.com/api/products?view=enterprise", timeout=15) as response:
                products = json.load(response)
            versions = [release["ProductVersion"]
                        for product in products if product.get("Product") == "Stable"
                        for release in product.get("Releases", [])
                        if release.get("Platform") == "Windows"
                        and release.get("Architecture") == "x64"
                        and re.fullmatch(r"\d+\.\d+\.\d+\.\d+", release.get("ProductVersion", ""))]
            version = max(versions, key=lambda item: tuple(map(int, item.split("."))))
        except (URLError, TimeoutError, OSError, ValueError, KeyError, TypeError):
            version = "155.0.4283.45"
            print("Catálogo Edge indisponível; usando a versão validada 155.0.4283.45.", flush=True)

    major = version.split(".")[0]
    constants.CHROMIUM_FULL_VERSION = version
    constants.CHROMIUM_MAJOR_VERSION = major
    constants.SEC_MS_GEC_VERSION = communicate.SEC_MS_GEC_VERSION = voices.SEC_MS_GEC_VERSION = "1-" + version
    base = "api.msedgeservices.com/tts/cognitiveservices"
    token = constants.TRUSTED_CLIENT_TOKEN
    constants.WSS_URL = communicate.WSS_URL = f"wss://{base}/websocket/v1?Ocp-Apim-Subscription-Key={token}"
    constants.VOICE_LIST = voices.VOICE_LIST = f"https://{base}/voices/list?Ocp-Apim-Subscription-Key={token}"
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        f"(KHTML, like Gecko) Chrome/{major}.0.0.0 Safari/537.36 Edg/{major}.0.0.0"
    )
    for headers in (constants.BASE_HEADERS, constants.WSS_HEADERS, constants.VOICE_HEADERS,
                    communicate.WSS_HEADERS, voices.VOICE_HEADERS):
        headers["User-Agent"] = user_agent
    communicate.WSS_HEADERS["Sec-WebSocket-Protocol"] = "synthesize"
    voices.VOICE_HEADERS["Authority"] = "api.msedgeservices.com"
    voices.VOICE_HEADERS["Sec-CH-UA"] = (
        f'" Not;A Brand";v="99", "Microsoft Edge";v="{major}", "Chromium";v="{major}"'
    )
    for module in (communicate, voices):
        context = getattr(module, "_SSL_CTX", None)
        if context is not None:
            context.load_default_certs()
    _EDGE_CONFIGURED = True
    print(f"Voz {VOICE}: conexão Edge Services, versão {version}, sem chave Azure.", flush=True)


async def synthesize(text: str, destination: Path) -> None:
    """Use Edge TTS with retries, then local Brazilian Portuguese speech as fallback."""
    try:
        import edge_tts
        from aiohttp import ClientError

        if not _EDGE_CONFIGURED:
            await asyncio.to_thread(configure_edge)

        temporary = destination.with_name(destination.name + ".parcial.mp3")
        waits = (5, 10, 20)
        for attempt in range(len(waits) + 1):
            try:
                temporary.unlink(missing_ok=True)
                communicator = edge_tts.Communicate(
                    text, VOICE, rate=RATE, connect_timeout=30, receive_timeout=90,
                )
                await communicator.save(str(temporary))
                if not temporary.exists() or temporary.stat().st_size == 0:
                    raise edge_tts.exceptions.NoAudioReceived("Áudio vazio.")
                if probe_duration(temporary) <= 0:
                    raise ValueError("Áudio da voz Antonio sem duração.")
                temporary.replace(destination)
                return
            except (ClientError, asyncio.TimeoutError, edge_tts.exceptions.NoAudioReceived) as error:
                temporary.unlink(missing_ok=True)
                if attempt == len(waits):
                    print(
                        f"Edge TTS falhou após {attempt + 1} tentativas ({error}). "
                        "Usando a voz local pt-br para concluir o vídeo.", flush=True
                    )
                    break
                wait = waits[attempt]
                print(f"Voz Antonio: tentativa {attempt + 1} falhou ({type(error).__name__}); nova tentativa em {wait}s.", flush=True)
                await asyncio.sleep(wait)
            except Exception:
                temporary.unlink(missing_ok=True)
                raise
    except ImportError as error:
        print(f"Edge TTS indisponível ({error}). Usando a voz local pt-br.")

    local_wav = destination.with_name(f"{destination.stem}_local.wav")
    run([
        "espeak-ng", "-v", "pt-br", "-s", "165",
        "-w", str(local_wav), text,
    ])
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(local_wav), "-codec:a", "libmp3lame", "-q:a", "3",
        str(destination),
    ])


def probe_duration(path: Path) -> float:
    output = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        text=True,
    ).strip()
    return float(output)


def convert_to_wav(source: Path, destination: Path) -> None:
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source), "-ar", "48000", "-ac", "2",
        "-c:a", "pcm_s16le", str(destination),
    ])


def build_segment(frame_path: Path, audio_path: Path, output_path: Path, duration: float) -> None:
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(frame_path),
        "-i", str(audio_path), "-t", f"{duration:.3f}", "-map", "0:v:0", "-map", "1:a:0",
        "-vf", "format=yuv420p", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-shortest", str(output_path),
    ])


def build_typewriter_segment(frame_dir: Path, audio_path: Path, output_path: Path,
                            duration: float, frame_rate: int = 8) -> None:
    pattern = str(frame_dir / "%04d.jpg")
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-framerate", str(frame_rate), "-i", pattern, "-i", str(audio_path),
        "-t", f"{duration:.3f}", "-map", "0:v:0", "-map", "1:a:0",
        "-vf", f"fps={FPS},tpad=stop_mode=clone:stop_duration={duration:.3f},format=yuv420p", "-r", str(FPS), "-c:v", "libx264",
        "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "192k",
        "-ar", "48000", "-ac", "2", "-af", f"apad=pad_dur={duration:.3f}", "-shortest", str(output_path),
    ])


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "_", normalized.lower()).strip("_")[:64] or "pergunta"


def resolve_image(value: str | None) -> Path | None:
    if not value:
        return None
    path = (ROOT / value).resolve()
    if ROOT not in path.parents:
        raise ValueError("O caminho da imagem precisa ficar dentro do repositório.")
    if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise ValueError(f"Formato de imagem não suportado: {path.suffix}")
    return path


def validate(question: dict, index: int) -> None:
    required = ("pergunta", "verdadeiro", "explicacao", "legenda", "hashtags")
    missing = [field for field in required if field not in question]
    if missing:
        raise ValueError(f"Pergunta {index}: faltam os campos {', '.join(missing)}.")
    if not isinstance(question["pergunta"], str) or not question["pergunta"].strip():
        raise ValueError(f"Pergunta {index}: o campo pergunta precisa ter texto.")
    if not isinstance(question["verdadeiro"], bool):
        raise ValueError(f"Pergunta {index}: verdadeiro precisa ser True ou False.")
    if not isinstance(question["explicacao"], str) or not question["explicacao"].strip():
        raise ValueError(f"Pergunta {index}: escreva uma explicação.")
    if not isinstance(question["legenda"], str) or not question["legenda"].strip():
        raise ValueError(f"Pergunta {index}: escreva a legenda para publicação.")
    tags = question["hashtags"]
    if not isinstance(tags, list) or not 1 <= len(tags) <= 4:
        raise ValueError(f"Pergunta {index}: informe de 1 a 4 hashtags relacionadas ao tema.")
    if any(not isinstance(tag, str) or not tag.startswith("#") or len(tag) < 2 for tag in tags):
        raise ValueError(f"Pergunta {index}: cada hashtag deve começar com #.")


def format_caption(question: dict) -> str:
    tags = " ".join(question["hashtags"])
    return f"CAPA_SEGUNDOS=2\n\n{question['legenda'].strip()}\n{tags}\n"


def make_one_video(index: int, question: dict, send_drive: bool = False, batch: str = "manual", palette: dict | None = None) -> tuple[Path, Path]:
    validate(question, index)
    palette = palette or PALETTES[((index - 1) // 3) % len(PALETTES)]
    image_path = resolve_image(question.get("imagem"))
    answer_label = "verdadeira" if question["verdadeiro"] else "falsa"
    answer_text = f"A resposta é {answer_label}. {question['explicacao']}"
    base_name = f"{index:02d}_{slugify(question['pergunta'])}"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="juh_vf_") as temp_dir:
        temp = Path(temp_dir)
        question_audio_mp3 = temp / "pergunta.mp3"
        answer_audio_mp3 = temp / "resposta.mp3"
        asyncio.run(synthesize(question["pergunta"], question_audio_mp3))
        asyncio.run(synthesize(answer_text, answer_audio_mp3))
        question_audio = temp / "pergunta.wav"
        answer_audio = temp / "resposta.wav"
        convert_to_wav(question_audio_mp3, question_audio)
        convert_to_wav(answer_audio_mp3, answer_audio)

        frames: list[Path] = []
        audios: list[Path] = []
        durations: list[float] = []
        question_frame = temp / "pergunta.png"
        render_question_frame(question, image_path, palette).save(question_frame)
        frames.append(question_frame)
        audios.append(question_audio)
        durations.append(probe_duration(question_audio))

        for count in (3, 2, 1):
            frame_path = temp / f"contagem_{count}.png"
            render_question_frame(question, image_path, palette, countdown=count).save(frame_path)
            beep_path = temp / f"bip_{count}.wav"
            write_beep(beep_path)
            frames.append(frame_path)
            audios.append(beep_path)
            durations.append(1.0)

        segments: list[Path] = []
        for part, (frame, audio, duration) in enumerate(zip(frames, audios, durations, strict=True), start=1):
            segment = temp / f"segmento_{part:02d}.mp4"
            build_segment(frame, audio, segment, duration)
            segments.append(segment)

        answer_duration = probe_duration(answer_audio)
        answer_frames = temp / "resposta_frames"
        answer_frames.mkdir()
        frame_rate = 8
        # Reserve the final second as a still frame so the complete last word
        # remains visible instead of disappearing on the video's last frame.
        typing_duration = max(1.0, len(question["explicacao"].strip()) / 15.0)
        frame_count = max(1, math.ceil(typing_duration * frame_rate))
        explanation = question["explicacao"].strip()
        answer_base = render_answer_frame(question, image_path, palette, " ")
        for frame_no in range(frame_count):
            visible_chars = min(len(explanation), round(len(explanation) * (frame_no + 1) / frame_count))
            frame_path = answer_frames / f"{frame_no + 1:04d}.jpg"
            render_answer_frame(question, image_path, palette, explanation[:visible_chars], answer_base,
                                explanation).save(
                frame_path, quality=88, optimize=True
            )
        answer_segment = temp / "segmento_resposta.mp4"
        build_typewriter_segment(answer_frames, answer_audio, answer_segment, max(answer_duration, typing_duration), frame_rate)
        segments.append(answer_segment)

        concat_file = temp / "segmentos.txt"
        concat_file.write_text("".join(f"file '{segment.as_posix()}'\n" for segment in segments), encoding="utf-8")
        video_path = OUTPUT_DIR / f"{base_name}.mp4"
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_file), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k",
            "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(video_path),
        ])

    caption_path = OUTPUT_DIR / f"{base_name}.txt"
    result_word = "Verdadeiro" if question["verdadeiro"] else "Falso"
    caption_path.write_text(format_caption(question), encoding="utf-8")
    if send_drive:
        run([
            "rclone", "copyto", str(video_path),
            f"{DRIVE_BASE}/execucao-{batch}/{video_path.name}",
        ])
        run([
            "rclone", "copyto", str(caption_path),
            f"{DRIVE_BASE}/execucao-{batch}/{caption_path.name}",
        ])
    return video_path, caption_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera vídeos Juh Quiz de Verdadeiro ou Falso.")
    parser.add_argument("--enviar-drive", action="store_true", help="envia MP4 e TXT para o Drive do Quiz-13")
    parser.add_argument("--lote", default=None, help="identificador da pasta de execução no Drive")
    args = parser.parse_args()

    require_program("ffmpeg")
    require_program("ffprobe")
    if args.enviar_drive:
        require_program("rclone")
    if not PERGUNTAS:
        raise ValueError("Adicione pelo menos uma pergunta em dados_vf.py.")
    batch = args.lote or "manual"
    for index, question in enumerate(PERGUNTAS, start=1):
        palette = PALETTES[((index - 1) // 3) % len(PALETTES)]
        video, caption = make_one_video(index, question, args.enviar_drive, batch, palette)
        print(f"Criado: {video.name} e {caption.name}")
        if args.enviar_drive:
            print(f"Enviado ao Drive: {DRIVE_BASE}/execucao-{batch}/")


if __name__ == "__main__":
    main()
