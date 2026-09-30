# yt-to-mp3

Baixa o áudio de um vídeo do YouTube e converte para MP3 (yt-dlp + ffmpeg).
Use apenas com conteúdo que você tem autorização para baixar.

## ⚡ Já configurei tudo — copia e cola

Rodar com o vídeo padrão (defina o link em `DEFAULT_URL`, no topo de `yt_to_mp3.py`):

```bash
cd ~/Documents/coding/study/yt-to-mp3
source .venv/bin/activate
python yt_to_mp3.py
```

Rodar com **outro link** (é aqui que você coloca o link 👇):

```bash
cd ~/Documents/coding/study/yt-to-mp3
source .venv/bin/activate
python yt_to_mp3.py "COLE_O_LINK_AQUI"
```

Com interface web (abre em http://localhost:8000 e você cola o link na página):

```bash
cd ~/Documents/coding/study/yt-to-mp3
source .venv/bin/activate
python app.py
```

Os MP3s ficam na pasta `downloads/`.

## Primeira instalação (macOS)

```bash
brew install ffmpeg deno
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- `ffmpeg`: converte para MP3.
- `deno`: runtime JS que o yt-dlp usa para resolver o desafio do YouTube.

## Opções da linha de comando

| Opção | O que faz | Exemplo |
|---|---|---|
| `URL...` | um ou mais links | `python yt_to_mp3.py URL1 URL2` |
| `-o` | pasta de saída (padrão `downloads`) | `-o musicas` |
| `-q` | qualidade em kbps: 128, 192, 320 | `-q 320` |
| `-b` | navegador logado no YouTube, para cookies (padrão `chrome`) | `-b safari` |
| `--cookies` | arquivo `cookies.txt` em vez do navegador | `--cookies cookies.txt` |

## Vídeos com restrição de idade

O YouTube exige login. O script usa os cookies do Chrome por padrão, então fique
logado no YouTube nele. Para outro navegador, use `-b` ou mude `DEFAULT_BROWSER`
em `yt_to_mp3.py`. No Safari/Firefox pode ser preciso dar *Full Disk Access* ao Terminal
(System Settings → Privacy & Security).

## Problemas comuns

- `ffmpeg não encontrado` → `brew install ffmpeg`
- `n challenge solving failed` → `brew install deno` e `pip install -U -r requirements.txt`
- `pip: command not found` → ative a venv com `source .venv/bin/activate`
