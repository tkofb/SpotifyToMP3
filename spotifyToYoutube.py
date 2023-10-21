import os
import json
import requests
from getPlaylist import Songs
from pytube import YouTube
from youtubesearchpython import *

class YoutubeConversion(Songs):
    def __init__(self):
        super().__init__()
        self.askForPlaylistToDownload()
        self.specificPlaylistSongDict(self.chosenPlaylist)
        
        self.getYoutubeURLS()
    
    def getYoutubeURLS(self):
        self.songToYoutube = dict()
        songCount = 0
        
        for songName in self.youtubeQuery.values():
            
            songList = VideosSearch(songName, limit=4).result()
            
            songCount += 1
            
            videoId = songList['result'][0]['id']
            
            youtubeUrl = "https://www.youtube.com/watch?v=" + videoId
            
            self.songToYoutube[songCount] = youtubeUrl
            
            print(f'{songName} found ({songCount}/{len(self.youtubeQuery)})')
            
    def setFileName(self, name):
        self.fileName = name
    
    def askForFileName(self):
        name = input("What do you want to name the playlist? ")
        self.setFileName(name)
                    
    def downloadAllSongs(self):
        self.askForFileName()
        
        for songNumber, i in enumerate(self.songToYoutube.values()):
            try:
                currentSong,artist = self.downloadSong(i)
                print(f"Song: {currentSong} by {artist} finished downloading ({songNumber+1}/{len(self.youtubeQuery)})")
            except Exception as e:
                print(e)
            
    def downloadSong(self, youtubeLink):
        yt = YouTube(youtubeLink)
        song = yt.title

        audioOnlyStreams = yt.streams.filter(only_audio=True)
        firstStream = audioOnlyStreams[0]

        if '/' in song:
            song = song.replace('/','')

        firstStream.download(output_path = f'MusicDownloads/{self.fileName}', filename = f'{song}.mp3')
        
        return (yt.title,yt.author) 
         
if __name__ == "__main__":
    youtube = YoutubeConversion()
    youtube.downloadAllSongs()