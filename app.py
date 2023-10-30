'''Voice processor with voice and text translator'''
import tkinter as tk
import sqlite3
import datetime
from tkinter import PhotoImage
import pyttsx3
import speech_recognition as sr
from textblob import TextBlob

from PIL import Image, ImageTk


root = tk.Tk()
root.title("Procesador de Voz y Texto")
root.geometry("600x300")

# Cargar imágenes de íconos
image_recording = PhotoImage(file="icon_recording.png")
image_stop = PhotoImage(file="icon_stop.png")

# Configura el número de filas y columnas
root.grid_rowconfigure(3, weight=1)  # Configura 4 filas (0, 1, 2, 3)
root.grid_columnconfigure(2, weight=1)  # Configura 3 columnas (0, 1, 2)

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

recording = False

ID1 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0"
ID2 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
ID3 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
ID4 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-MX_SABINA_11.0"

def save_textlog(text):
    '''save_textlog'''
    with open("transcription/log_rec.txt", "a", encoding="utf-8") as file:
        # Escribe el texto que deseas agregar al archivo
        new_text = f"{datetime.datetime.now()} - {text}\n"
        file.write(new_text)

# escuchar micro y devolver audio como texto
def voice_to_text():
    '''voice_to_text'''
    global recording
    # almacenar recognizer en variable
    recon = sr.Recognizer()
    if not recording:
        with sr.Microphone() as origen:
            record_voice_button.config(image=image_stop)
            # tiempo de espera
            recon.pause_threshold = 0.5
            # limpiar ruido
            recon.adjust_for_ambient_noise(origen, duration=1)

            try:
                print("Escuchando...")
                status_label.config(text="Escuchando...")
                # escuchar audio
                audio = recon.listen(origen)

                # convertir audio a texto
                text = recon.recognize_google(audio, language="es-ES")
                save_textlog(text)
                # mostar audio
                audio_label.config(text=text)
                # guardar audio
                datime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                namefile = f'recorder/voice_to_text{datime}.mp3'
                with open(namefile, "wb") as file:
                    file.write(audio.get_wav_data())
            except sr.UnknownValueError as error:
                print(error)
                status_label.config(text="No entendí, intenta de nuevo")
                print("No entendí, intenta de nuevo")
            except sr.RequestError as error:
                print(error)
                status_label.config(text="No hay servicio")
                print("No hay servicio")
            finally:
                print("Fin de la grabación")
                status_label.config(text="Detenido")
                recording = False
                record_voice_button.config(image=image_recording)
    else:
        print("Ya se está grabando")
        status_label.config(text="Ya se está grabando")
        recording = True
        record_voice_button.config(image=image_recording)

# almacenar engine en variable
engine = pyttsx3.init()

def text_to_audio():
    '''text_to_audio'''
    text = text_entry.get("1.0", "end-1c")
    engine.setProperty("voice", ID1)
    # hablar
    engine.say(text)
    engine.runAndWait()
    # guardar en mp3
    namefileaudio = f'recorder/text_to_audio{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.mp3'
    engine.save_to_file(text, namefileaudio)
    save_textlog(text)

# Botón para iniciar la grabación de voz
record_voice_button = tk.Button(root, image=image_recording, command=voice_to_text)
record_voice_button.grid(row=0, column=0, padx=10, pady=10)

# Etiqueta para mostrar el texto grabado en audio
status_label = tk.Label(root, text="Inicio")
status_label.grid(row=1, column=0, padx=10, pady=10,  sticky="w")

# Etiqueta para mostrar el texto grabado en audio
audio_label = tk.Label(root, text="")
audio_label.grid(row=2, column=0, padx=10, pady=10,  sticky="w")

# Configura el cuadro de texto para ocupar el 75% del ancho y alineado a la izquierda
text_entry = tk.Text(root, height=5, width=60)  # 5 líneas de alto, ancho mínimo
text_entry.grid(row=3, column=0, padx=10, pady=10,  sticky="w"+"s")

# Botón para convertir texto en voz
text_to_voice_button = tk.Button(root, text="Texto a Voz", command=text_to_audio)
text_to_voice_button.grid(row=3, column=1, padx=10, pady=10, sticky="w"+"s")

root.mainloop()
