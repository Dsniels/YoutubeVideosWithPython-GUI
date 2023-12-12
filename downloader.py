from pytube import YouTube
from pytube import Playlist
from tqdm import tqdm
import os

def download(url, output_path="downloads"):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video_file = video.download(output_path=output_path + "/Videos")
    except Exception as e:
        print(f"Ocurrió un error durante la descarga: {e}")

def download_playlist(playlist_url, output_path="downloads"):
    try:
        playlist=Playlist(playlist_url)
        print(f"Descargando Playlist: {playlist.title}")

        for video_url in tqdm(playlist.video_urls, desc="Descargando"):
            download(video_url, output_path)

        print("Descarga completa")
    except Exception as e :
        print("Ocurrio un error")


if __name__ == "__main__":

    print("Seleccione la opcion a descargar: 1.Video    2.Playlist")
    opcion = input()
    
    match opcion:
        case "1":
            link = input("Ingrese la liga del video: ")       
            download(link)
            print("Descarga finalizada.")
        case "2":
            playlist_url = input("Ingrese el enlace de la playlist de YouTube: ")
            download_playlist(playlist_url)
        case _:
            print("Opcion no existente")


    
