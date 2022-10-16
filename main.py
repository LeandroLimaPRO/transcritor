'''
PARA LINUX INSTALAR DEPENDENCIA apt-get install ffmpeg libavcodec-extra
para WINDOWS, COLOCAR CODEC FFMPEG NA RAIZ C: E ADICIONAR A PASTA BIN AO PATHENV DO WINDOWS

passo 1: pip install -r requirements.txt

passo 2: uvicorn main:app --reload
'''
import json
import os
from os.path import exists
import shutil
import moviepy.editor as mp
import speech_recognition as sr
import moviepy.editor as mp
import sys
from pydub import AudioSegment
from fastapi import FastAPI, File, UploadFile

#a variável path contem o nome do arquivo do seu vídeo
NOME_ARQUIVO = "audiotallos" 


#path = f"{NOME_ARQUIVO}.mp3"
def para_texto(nomedoarquivo, save_on_file = False):
    src=f"{nomedoarquivo}.mp3"
    if exists(src):
        # converter de mp3 para wav
        sound = AudioSegment.from_file(src, "mp3")
        sound.export(f"{nomedoarquivo}.wav", format="wav")
        file_audio = sr.AudioFile(f"{nomedoarquivo}.wav")


        # use the audio file as the audio source
        r = sr.Recognizer()
        with file_audio as source:
            audio_text = r.record(source)
            text = r.recognize_google(audio_text,language='pt-BR')
            
            if save_on_file:
                arq = open(f"{nomedoarquivo}.txt","w")
                arq.write(text)
                arq.close()
            print(text)
            return text
    else:
        return None

## micro serviço
app = FastAPI()

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File()):
    #print(file.filename)
    name = file.filename.split(".")
    #print(name)
    file_location = f"./{file.filename}"
    with open(file_location, "wb+") as buffer:
        print(file.file)
        shutil.copyfileobj(file.file, buffer)  
    texto = para_texto(name[0])
    if texto != None:
        return {"filename": file.filename, "texto":texto}
    else:
        return {"erro": "Não foi possivel ober texto"}