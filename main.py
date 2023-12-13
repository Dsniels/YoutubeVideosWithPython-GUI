import tkinter 
import customtkinter
from pytube import YouTube
from pytube import Playlist
import threading
import ssl
import os
import re


#Descarga de video
ssl._create_default_https_context = ssl._create_unverified_context

def start_download_thread():
    title.configure(text="")
    percentage.configure(text="0%")
    finishLabel.configure(text="")
    progressBar.set(0)
    download_thread = threading.Thread(target=download_video)
    download_thread.daemon = True  
    download_thread.start()  
    percentage.pack()
    progressBar.pack(padx=10, pady=10)

def download_video():
    
    try:
        title.configure(text="") 
        url = URL.get()

        if "youtube.com/playlist" in url:
            progressBar.pack_forget()
            percentage.pack_forget()
            p = Playlist(url)
            total_videos = len(p.video_urls)
            current_video = 0
            for video_url in p.video_urls:
                
                current_video += 1
                finishLabel.configure(text=f"Espere...Descargando video {current_video} de {total_videos}")
        
                yt = YouTube(video_url)
                invalid_chars = r'<>:"/\|?*'
                cleaned_title = re.sub(f'[{re.escape(invalid_chars)}]', '', yt.title)  # Eliminar caracteres inválidos
                if music.get():
                    video = yt.streams.filter(only_audio=True).first()
                    filename = f"{cleaned_title}.mp3"
                else:
                    video = yt.streams.get_highest_resolution()
                    filename = f"{cleaned_title}.mp4"
                
                title.configure(text=yt.title, text_color="white")
                video.download(filename=filename, output_path=output_path_playlist)
    
            finishLabel.configure(text="Descargado!")
            progressBar.pack_forget()
        else:
            yt = YouTube(url, on_progress_callback=on_progress)
            if(music.get()):
                video = yt.streams.filter(only_audio=True).first() 
                video = yt.streams.get_audio_only()
                filename=f"{video.title}.mp3"
            else:
                video = yt.streams.get_highest_resolution()
                filename=f"{video.title}"
               

            title.configure(text=yt.title, text_color="white")
            finishLabel.configure(text="",text_color="white")
            video.download(filename=filename, output_path=output_path)
            finishLabel.configure(text="Descargado!")
        URL.set("")
        title.configure(text="")
 

    except Exception as e:
        finishLabel.configure(text=f"Error {e}", text_color="red")




def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    percentage.configure(text=per + '%')
    percentage.update()
    progressBar.set(float(percentage_of_completion) / 100)




#Configuration de interfaz
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

#Configuracion de descarga
desktop_path = os.path.join(os.path.expanduser('~'), 'OneDrive\Desktop')
output_path = os.path.join(desktop_path, 'YouTubeVideos')
os.makedirs(output_path, exist_ok=True)
output_path_playlist = os.path.join(desktop_path, 'Playlist')

#app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Youtube")

frame = customtkinter.CTkFrame(master=app,
                               width=200,
                               height=200,
                               corner_radius=10)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

#Elementos UI
title = customtkinter.CTkLabel(frame,text="Ingrese el link del video", 
                                compound = "center",
                                anchor= "center")
title.pack(padx=10, pady=20)





music = customtkinter.BooleanVar()
check_music = customtkinter.CTkCheckBox(frame, text="Audio",variable=music, onvalue=True, offvalue=False)
check_music.pack(side="top", anchor="w",padx=5, pady=5)



#Link input
URL = tkinter.StringVar()
link = customtkinter.CTkEntry(frame, width=350, height=40, textvariable=URL)
link.pack(padx=10)

#Download button
download_button = customtkinter.CTkButton(frame, text="Descargar", command=start_download_thread)
download_button.pack(padx=10, pady=10)


#Download finished
finishLabel = customtkinter.CTkLabel(frame, text="")
finishLabel.pack()


#progress bar
percentage = customtkinter.CTkLabel(frame, text="0%")
percentage.pack_forget()
progressBar = customtkinter.CTkProgressBar(frame, width=400)
progressBar.set(0)
progressBar.pack_forget()


#Run app
app.mainloop()