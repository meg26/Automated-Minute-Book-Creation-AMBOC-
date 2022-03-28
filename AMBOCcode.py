# import modules
import traceback
import torch
import json 
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import os 
import speech_recognition as sr
from pydub import AudioSegment
from pydub import AudioSegment, effects  
from pydub.silence import split_on_silence
import speaker_verification_toolkit.tools as svt #Importing Library
import numpy

#Starting Frontend
import webbrowser
import codecs
webbrowser.open('C:\\Users\\LENOVO\\Code\\Python_WorkSpace\\menu.html')

#Configuring Summarization Module
model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')
device = torch.device('cpu')


#Audio Sample Creation
def sample_creation():
    names=[]
    fv=[]
    path = 'C:\\Users\\LENOVO\\Code\\Python_WorkSpace\\Samples3'  # Path =to samples
    folder = os.fsencode(path)
    count=0
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        new_name=""
        for a in filename:
            if(a=='_'):
                break
            else:
                new_name+=a
        if(new_name in names):
            continue
        else:
            try:
                names.append(new_name)
                path="C:\\Users\\LENOVO\\Code\\Python_WorkSpace\\Samples3\\"+filename
                a=svt.extract_mfcc_from_wav_file(path,16000,0.025,0.01)
                fv.append(a)
                count=count+1
                if(count%5==0):
                    print("Done"+str(count))
                print(new_name+" has worked "+filename)
            except:
                print(new_name+" didnt work.")
                traceback.print_exc()
    return fv,names



#Speech To Text
def load_chunks(filename,fv,names):
    recognizer = sr.Recognizer()
    paras=[]
    Transcript=[]
    long_audio = AudioSegment.from_wav(filename)
    chunks = split_on_silence(
        long_audio, min_silence_len=2000,
        silence_thresh=-40
    )
    print(len(chunks))
    fh = open("Transcript.txt", "w+")
    try:
        os.mkdir('audio_chunks')
    except(FileExistsError):
        pass
    print('Inside audio_chunks')
    i=0
    for chunk in chunks:
        chunk_silent = AudioSegment.silent(duration = 1500)
        audio_chunk = chunk_silent + chunk + chunk_silent
        #Saving Chunk
        audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav")
        filename='chunk'+str(i)+'.wav'
        #Processing chunks
        Transcript=speakerveri(i,fv,names,Transcript)
        file = filename
        r = sr.Recognizer()
        with sr.AudioFile(file) as source:
            r.adjust_for_ambient_noise(source)
            audio_listened = r.listen(source)
        try:
            rec = r.recognize_google(audio_listened)
            print(rec)
            fh.write(rec+". ")
            paras.append(rec)
            Transcript.append(rec)
        except sr.UnknownValueError:
            print("Could not understand audio")
            Transcript.append("""<br>Could not understand audio""")
        except sr.RequestError as e:
            print("Could not request results. check your internet connection")
        except:
            print("Could not understand audio")
            Transcript.append("<br>Could not understand audio")

        i=i+1
    print("____________________________________________________________________________________________________")
    minutes=summary(paras)
    os.chdir('..')
    return Transcript,minutes
    

#Speaker Verification
def speakerveri(i,fv,names,Transcript):
    distance=[]
    #Creating feature vector of audio to be tested
    path2='chunk'+str(i)+'.wav'
    #Test mfcc
    Test=svt.extract_mfcc_from_wav_file(path2,16000,0.025,0.01)
    for a in fv:
        x=svt.compute_distance(a,Test)
        distance.append(int(x))
    min_value = min(distance)
    min_index = distance.index(min_value)
    print('\n--------------------------------------------')
    Transcript.append("""<hr style="border-top: 0.5px solid blue;">""")
    Transcript.append("""<br><center>The voice belongs to <b style= "color:#1434A4;">"""+names[min_index]+"""</b></center><br> """)
    return Transcript

#Text Summarization    
def summary(paras):
    minutes=""
    for i in paras:
        text=i
        preprocess_text = text.strip().replace("\n","")
        t5_prepared_Text = "summarize: "+preprocess_text

        tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)


        # summmarize 
        #print("\nmax length"+str(int(len(text)*3/4)))
        #print("\nmin length" +str(int(len(text)/10))+"\n")
        summary_ids = model.generate(tokenized_text,
                                     num_beams=4,
                                     no_repeat_ngram_size=2,
                                     min_length=int(len(text)/10),
                                     max_length=int(len(text)*3/4),
                                     early_stopping=False)

        output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        output=output+". "
        minutes=minutes+output
        #print(output)
    print ("\n\n\033[1m Summarized text: \033[0m \n")
    print(minutes)
    return minutes
os.chdir('C:\\Users\\LENOVO\\Code\\Python_WorkSpace')
cwd = os.getcwd()
print(cwd)
result=sample_creation()
fv=result[0]
names=result[1]
print(names)
Out=load_chunks('All_Final.wav',fv,names)
Transc = ' '.join(map(str, Out[0]))
print('Completed Creating Minutes')


#frontend_S
f = open('C:\\Users\\LENOVO\\Code\\Python_WorkSpace\\portfolio1.html', 'w')
  
#Front end html
html_template = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Meeting Minutes</title>
   
    <link href='https://fonts.googleapis.com/css?family=Merriweather' rel='stylesheet'>
    <link href='https://fonts.googleapis.com/css?family=Open Sans' rel='stylesheet'>
    <link rel="stylesheet" href="portfolio1.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="fontawesome-free-5.15.3-web/fontawesome-free-5.15.3-web/css/all.css">
    <title>home</title>
    <style>
      h1{
        text-align: center;
      }


.amboc{
  font-family: "Times New Roman", Times, serif;
}

    </style>
  </head>

  <body style="overflow-x: hidden;background-color:white;">
    <nav class="navbar navbar-expand-lg navbar-light" style="background-color: whitesmoke">
        <a class="navbar-brand" href="#"><i class="fab fa-atlassian"> AMBOC</i></a>
        <div class="collapse navbar-collapse" id="navbarText">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
              <a class="nav-link" href="menu.html">Home <span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="upload.html">Voice Sample upload</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="upload1.html">Meeting Recording upload</a>
            </li>
          </ul>
        </div>
      </nav>
<div class="main">
<div class="card">
<div class="y" style="z-index=-1;font-size:20px;padding:10px;">
 <b><center>Meeting Transcript</center></b><br>"""+Transc+"""
</div>
</div>
<div class="card">
<div class="x" style="z-index=-1;font-size:20px;padding:10px;">
 <b><center>Meeting Minutes</center></b><br>"""+Out[1]+"""
</div>
</div>
</div>
<div class="sidebar"></div>
</body>
</html>

"""
#frontend_S  
f.write(html_template)
f.close()
webbrowser.open('C:\\Users\\LENOVO\\Code\\Python_WorkSpace\\portfolio1.html',new=0) 


