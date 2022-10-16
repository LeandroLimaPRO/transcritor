# API PARA TRANSCRIÇÃO DE AUDIO

Api destinada para transcrição de audio, para mais informações ao iniciar vá para /docs ou /redocs

## Dependências

* PARA LINUX INSTALAR DEPENDENCIA `apt-get install ffmpeg libavcodec-extra`

* para WINDOWS, COLOCAR CODEC FFMPEG NA RAIZ C: E ADICIONAR A PASTA BIN AO PATHENV DO WINDOWS

### Instalação e uso

passo 1: `pip install -r requirements.txt`

passo 2: `uvicorn main:app --reload`