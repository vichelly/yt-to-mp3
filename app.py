#!/usr/bin/env python3
"""Interface web local para o yt_to_mp3. Rode: python app.py  e abra http://localhost:8000"""
import json
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from yt_to_mp3 import DEFAULT_BROWSER, baixar_mp3

PASTA = "downloads"
PORTA = 8000

HTML = """<!doctype html>
<html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>YouTube → MP3</title>
<style>
 body{font-family:system-ui,sans-serif;background:#0f1115;color:#e8e8e8;display:grid;place-items:center;min-height:100vh;margin:0}
 main{width:min(520px,92vw);background:#181b22;padding:28px;border-radius:14px}
 h1{margin:0 0 18px;font-size:22px}
 input,select,button{width:100%;box-sizing:border-box;padding:12px;border-radius:8px;border:1px solid #333;background:#0f1115;color:inherit;font-size:15px;margin-bottom:12px}
 button{background:#e5484d;border:0;font-weight:600;cursor:pointer}
 button:disabled{opacity:.5;cursor:wait}
 #msg{min-height:24px;font-size:14px}
 a{color:#7cc4ff}
</style></head><body><main>
<h1>YouTube → MP3</h1>
<input id="url" placeholder="Cole o link do vídeo aqui" autofocus>
<select id="q"><option value="128">128 kbps</option><option value="192" selected>192 kbps</option><option value="320">320 kbps</option></select>
<button id="go">Baixar MP3</button>
<div id="msg"></div>
</main>
<script>
const $=id=>document.getElementById(id);
$('go').onclick=async()=>{
  const url=$('url').value.trim(); if(!url) return;
  $('go').disabled=true; $('msg').textContent='Baixando e convertendo… pode levar alguns segundos.';
  try{
    const r=await fetch('/download',{method:'POST',body:JSON.stringify({url,quality:$('q').value})});
    const d=await r.json();
    if(d.ok){ $('msg').innerHTML='Pronto! <a href="/files/'+encodeURIComponent(d.file)+'" download>Baixar '+d.file+'</a> (também salvo na pasta downloads/)'; }
    else $('msg').textContent='Erro: '+d.error;
  }catch(e){ $('msg').textContent='Erro: '+e; }
  $('go').disabled=false;
};
$('url').addEventListener('keydown',e=>{if(e.key==='Enter')$('go').click()});
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/html; charset=utf-8", extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            return self._send(200, HTML.encode())
        if self.path.startswith("/files/"):
            nome = os.path.basename(urllib.parse.unquote(self.path[len("/files/"):]))
            caminho = os.path.join(PASTA, nome)
            if os.path.isfile(caminho):
                with open(caminho, "rb") as f:
                    dados = f.read()
                quoted = urllib.parse.quote(nome)
                return self._send(200, dados, "audio/mpeg",
                                  {"Content-Disposition": f"attachment; filename*=UTF-8''{quoted}"})
        self._send(404, b"not found", "text/plain")

    def do_POST(self):
        if self.path != "/download":
            return self._send(404, b"not found", "text/plain")
        try:
            dados = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            caminho = baixar_mp3(dados["url"], PASTA, dados.get("quality", "192"), DEFAULT_BROWSER)
            resp = {"ok": True, "file": os.path.basename(caminho)}
        except Exception as e:  # mostra o erro na página
            resp = {"ok": False, "error": str(e)}
        self._send(200, json.dumps(resp).encode(), "application/json")


if __name__ == "__main__":
    print(f"Abra http://localhost:{PORTA}  (Ctrl+C para parar)")
    ThreadingHTTPServer(("127.0.0.1", PORTA), Handler).serve_forever()
