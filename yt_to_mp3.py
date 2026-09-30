#!/usr/bin/env python3
"""Baixa o áudio de um vídeo do YouTube e converte para MP3.

Uso:
    python yt_to_mp3.py                 # usa o vídeo padrão abaixo
    python yt_to_mp3.py <URL> [<URL>…]  # uma ou mais URLs
    python yt_to_mp3.py <URL> -o pasta -q 320

Requisitos: pip install -r requirements.txt  e  ffmpeg instalado no sistema.
Use apenas com conteúdo que você tem autorização para baixar.
"""
import argparse
import shutil
import sys

from yt_dlp import YoutubeDL

DEFAULT_URL = "https://youtu.be/_Ziy6mfT5eY"


def baixar_mp3(url: str, pasta: str = "downloads", qualidade: str = "192") -> None:
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg não encontrado. Instale: brew install ffmpeg (Mac) | sudo apt install ffmpeg (Linux) | winget install ffmpeg (Windows)")

    opcoes = {
        "format": "bestaudio/best",
        "outtmpl": f"{pasta}/%(title)s.%(ext)s",
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": qualidade,  # kbps
            },
            {"key": "FFmpegMetadata"},
        ],
    }
    with YoutubeDL(opcoes) as ydl:
        ydl.download([url])


def main() -> None:
    p = argparse.ArgumentParser(description="YouTube -> MP3")
    p.add_argument("urls", nargs="*", default=[DEFAULT_URL], help="URL(s) do vídeo")
    p.add_argument("-o", "--output", default="downloads", help="pasta de saída")
    p.add_argument("-q", "--quality", default="192", help="bitrate MP3 em kbps (128, 192, 320)")
    args = p.parse_args()

    for url in args.urls:
        baixar_mp3(url, args.output, args.quality)
    print(f"\nPronto! Arquivos em: {args.output}/")


if __name__ == "__main__":
    main()
