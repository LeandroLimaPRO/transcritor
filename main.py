'''
PARA LINUX INSTALAR DEPENDENCIA apt-get install ffmpeg libavcodec-extra
para WINDOWS, COLOCAR CODEC FFMPEG NA RAIZ C: E ADICIONAR A PASTA BIN AO PATHENV DO WINDOWS

passo 1: pip install -r requirements.txt

passo 2: uvicorn main:app --reload
'''
import json
import os
import re
import pdfplumber as pdf
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

class detect:
    def __init__(self):
        pass
    def detect(self,txt,regex):
        match = re.search(regex,txt)
        if match != None:
            return match.group()
        else:
            return None
    def find(self,txt,regex):
        result = re.findall(regex,txt)
        if result != None:
            return result
        else:
            return None

#path = f"{NOME_ARQUIVO}.mp3"
def audio_para_texto(nomedoarquivo, save_on_file = False):
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

def pdf_para_texto(nomedoarquivo,save_on_file =False):
    p = pdf.open(nomedoarquivo)
    d = detect()
    obj = {}
    pages = []
    cd = []
    tabelas = []
    for pag in p.pages:
        ttxt = pag.extract_tables()
        tabelas.append(ttxt)
        ttxt = pag.extract_text_simple()
        ptxt = pag.extract_text().split('\n')
        print(ttxt)
        for ln in ptxt:
            
            codigo_barra = d.detect(ln,'[0-9]{5}.[0-9]{5} [0-9]{5}.[0-9]{6} [0-9]{5}.[0-9]{6} [0-9]{1} [0-9]{14}')
            if codigo_barra != None:
                cd.append(codigo_barra)
        
        pages.append(ptxt)
    obj['conteudo'] = pages
    obj['tabelas'] = tabelas
    obj['codigo_barras']= cd
    return obj
    
## micro serviço
app = FastAPI()

@app.post("/audio/upload/")
async def create_upload_audio(file: UploadFile = File()):
    #print(file.filename)
    name = file.filename.split(".")
    #print(name)
    file_location = f"./{file.filename}"
    with open(file_location, "wb+") as buffer:
        print(file.file)
        shutil.copyfileobj(file.file, buffer)  
    texto = audio_para_texto(name[0])
    if texto != None:
        return {"filename": file.filename, "texto":texto}
    else:
        return {"erro": "Não foi possivel ober texto"}
    
    
@app.post("/pdf/upload/")
async def create_upload_pdf(file: UploadFile = File()):
    #print(file.filename)
    name = file.filename.split(".")
    #return {"filename": file.filename, "texto":'texto'}
    #print(name)
    file_location = f"./{file.filename}"
    with open(file_location, "wb+") as buffer:
        print(file.file)
        shutil.copyfileobj(file.file, buffer)  
        
    obj = pdf_para_texto(file_location)
    
    if obj != None:
        return {"filename": file.filename, "texto": obj}
    else:
        return {"erro": "Não foi possivel ober texto"}