from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from pytube import YouTube
import os
from tkinter.filedialog import askdirectory
from tkinter import *

class App():
    def __init__(self, url):
        self.url = url

        frame = Tk()
        frame.title("Youtube mp3 downloader")

        canvas = Canvas(frame, height=500,width=500)
        canvas.pack()

        top_frame = Frame(frame,bg="#f2f2f0")
        top_frame.place(relx=0.05,rely=0.03,relwidth=0.90,relheight=0.60)

        bottom_frame = Frame(frame,bg="#c6c7c5")
        bottom_frame.place(relx=0.05,rely=0.57,relwidth=0.90,relheight=0.39)

        general_title = Label(top_frame,bg="#f2f2f0",text="Youtube Mp3 Downloader",font=("Garamond",18,"bold"))
        general_title.pack(padx=10,pady=10,anchor="n")  

        url_title = Label(top_frame,bg="#c6c7c5",text="Please enter the music names with a comma",font=("Garamond",12,"bold"))
        url_title.pack(padx=10,pady=10,anchor="n")

        folder_button = Button(bottom_frame,text="Select Folder",font=("Garamond",12,"bold"),height=1,width=12,command=self.ask_directory)
        folder_button.pack(padx=10,pady=10,anchor="n")

        download_button = Button(bottom_frame,text="Download",font=("Garamond",12,"bold"),height=1,width=12,command=self.download)
        download_button.pack(padx=10,pady=10,anchor="n")

        self.video_folder_label = Label(bottom_frame,bg="#c6c7c5",fg="#737373",text="...",font=("Didot",12,"bold"))
        self.video_folder_label.pack(padx=10,pady=10,anchor="n")

        self.url_field = Text(top_frame,height=10,width=53)
        self.url_field.tag_configure('style',foreground="#bfbfbf",font=("Didot",10,"bold"))
        self.url_field.place(x=15,y=100)

        frame.mainloop()

    def create_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach",True)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.url)
        self.driver.maximize_window()
        time.sleep(2)

    def search(self):
        search_button = self.driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[2]/ytd-searchbox/form/div[1]/div[1]/input')
        time.sleep(0.5)
        self.urls = []

        for music in self.musics:
            search_button.send_keys(music)
            search_button.send_keys(Keys.ENTER)
            time.sleep(2)

            music = self.driver.find_element(By.XPATH, '//a[@class="yt-simple-endpoint style-scope ytd-video-renderer"]')
            music.click()
            time.sleep(2)
            current_url = self.driver.current_url
            self.urls.append(current_url)
            time.sleep(0.5)
            search_button.clear()
        
        self.driver.close()
    
    def ask_directory(self):
        self.folder = askdirectory()
        self.video_folder_label.config(text=self.folder)

    def download_musics(self):
        for url in self.urls:
            folder = self.video_folder_label.cget("text")
            my_music = YouTube(url)
            mp3 = my_music.streams.filter(only_audio=True).first()
            file = mp3.download(output_path=folder)
            base, ext = os.path.splitext(file)
            to_mp3 = base + ".mp3"
            os.rename(file,to_mp3)
    
    def convert(self):
        names = self.url_field.get("1.0","end").split(",")
        self.musics = names

    def download(self):
        self.convert()
        self.create_driver()
        self.search()
        self.download_musics()
    
url = "https://www.youtube.com/"
app = App(url)