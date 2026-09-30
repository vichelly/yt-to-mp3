#!/usr/bin/env python3
"""Baixa o áudio de um vídeo do YouTube e converte para MP3.

Uso:
    python yt_to_mp3.py                 # usa o vídeo padrão abaixo
    python yt_to_mp3.py <URL> [<URL>…]  # uma ou mais URLs
    python yt_to_mp3.py <URL> -o pasta -q 320
    python yt_to_mp3.py -b chrome       # vídeo com restrição de idade

Requisitos: pip install -r requirements.txt  e  ffmpeg instalado no sistema.
Use apenas com conteúdo que você tem autorização para baixar.
"""
import argparse
import shutil
import sys

from yt_dlp import YoutubeDL

DEFAULT_URL = "https://youtu.be/_Ziy6mfT5eY"
DEFAULT_BROWSER = "chrome"  # ex.: "safari" — navegador logado no YouTube (p/ vídeos com restrição de idade)


def baixar_mp3(url: str, pasta: str = "downloads", qualidade: str = "192", navegador: str | None = None, cookies: str | None = None) -> str:
    """Baixa e converte para MP3. Retorna o caminho do arquivo gerado."""
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg não encontrado. Instale: brew install ffmpeg (Mac) | sudo apt install ffmpeg (Linux) | winget install ffmpeg (Windows)")

    opcoes = {
        "format": "bestaudio/best",
        "outtmpl": f"{pasta}/%(title)s.%(ext)s",
        "noplaylist": True,
        # permite baixar o solver do desafio JS do YouTube (precisa de deno ou node instalado)
        "remote_components": ["ejs:github"],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": qualidade,  # kbps
            },
            {"key": "FFmpegMetadata"},
        ],
    }
    if cookies:
        opcoes["cookiefile"] = cookies
    elif navegador:
        # usa a sessão logada do navegador (necessário p/ vídeos com restrição de idade)
        # aceita "firefox" ou "firefox:/caminho/do/perfil"
        nome, _, perfil = navegador.partition(":")
        opcoes["cookiesfrombrowser"] = (nome, perfil) if perfil else (nome,)

    with YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info(url, download=True)
        return info["requested_downloads"][0]["filepath"]


def main() -> None:
    p = argparse.ArgumentParser(description="YouTube -> MP3")
    p.add_argument("urls", nargs="*", default=[DEFAULT_URL], help="URL(s) do vídeo")
    p.add_argument("-o", "--output", default="downloads", help="pasta de saída")
    p.add_argument("-q", "--quality", default="192", help="bitrate MP3 em kbps (128, 192, 320)")
    p.add_argument("-b", "--browser", default=DEFAULT_BROWSER,
                   help="usar cookies do navegador logado (chrome, firefox, safari, edge, brave) — p/ vídeos com restrição de idade")
    p.add_argument("--cookies", default=None, help="arquivo cookies.txt exportado do navegador (formato Netscape)")
    args = p.parse_args()

    for url in args.urls:
        baixar_mp3(url, args.output, args.quality, args.browser, args.cookies)
    print(f"\nPronto! Arquivos em: {args.output}/")


if __name__ == "__main__":
    main()
