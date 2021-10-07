from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

import os
from os import path
import sys
import urllib.request
import pafy
import humanize
from pafy import playlist


FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"main.ui"))


class MainApp(QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_Ui()
        self.handle_Buttons()
       
        
        

       
    #:::::::::::::::::Handle_Ui Function is Special For Styling Of Program:::::::::::::
    def handle_Ui(self):
        self.setWindowTitle("Downloader-SSAM")
        self.setWindowIcon(QIcon("download.png"))
        self.setFixedSize(900,600)
    
    #::::::::::::::::Handle_Button Function::::::::::::::::::::
    def handle_Buttons(self):
        self.pushButton.clicked.connect(self.Downlaod)
        self.pushButton_2.clicked.connect(self.handle_Browse)
        #pushButton Link With Search button:::
        self.pushButton_5.clicked.connect(self.Get_from_Youtube)
        #PushButton Download to me the video that i Choose:::
        self.pushButton_4.clicked.connect(self.Download_from_Youtube)
        #:::::::::::::::::::Two Button Linked By One Function:::::::::::::::::::::::::
        self.pushButton_3.clicked.connect(self.save_Browse_File)
        self.pushButton_7.clicked.connect(self.save_Browse_File)
        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        self.pushButton_6.clicked.connect(self.PlayList_Videos)
    
    #:::::::::::::::handle_Browse Function:::::::::
    def handle_Browse(self):
        save_Place = QFileDialog.getSaveFileName(self, caption="Save AS",directory=".",filter="All files (*.*)") 
        text=str(save_Place)
        name_dir=text[2:].split(",")[0].replace("'" , '')
        self.lineEdit_2.setText(name_dir)

    #::::::::::::::::handle_Progress Function:::::::::::::::
    def handle_Progress(self,blocknum,blocksize,totalsize):

        read = blocknum * blocksize 
        
        if totalsize > 0 :
            percent= read * 100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()#Not Responding

    #::::::::::::::::::::Download Function::::::::::::::::::::

    def Downlaod(self):
        #urllib library take from me three things:::1=>location::2=>url::3=>Progress
        url=self.lineEdit.text()
        save_location=self.lineEdit_2.text()
        try:
            urllib.request.urlretrieve(url,save_location,self.handle_Progress())
        except Exception:
            QMessageBox.warning(self,"downloading Error","downalod Failed")
        QMessageBox.information(self,"Downalod Completed !","Finished Downloading")
        self.progressBar.setValue(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
    #::::::::::::::::this Function Got me The infromation of youtube video and it's Quality::::::::::::::
    def Get_from_Youtube(self):
        try:
            video_link=self.lineEdit_3.text()
            v=pafy.new(video_link)
            # print(v.thumb)
            # print(v.title)
            # print(v.author)
            # print(v.bigthumb)
            # print(v.keywords)
            # print(v.duration)
            # print(v.rating)
            stream=v.allstreams
            # l=stream.split("[]")
           
            for l in stream:
                size=humanize.naturalsize(l.get_filesize())
                data="{} {} {} {} ".format(l.mediatype,l.extension,l.quality,size)
                self.comboBox.addItem(data)
          
        except ImportError as e:
            print(e)
    #:::::::::::::::this Function make to Get Location From User's Donwload File:::::::::::::::::
    #::::::::::::::it's Private of Youtube Tub:::::::
    def save_Browse_File(self):
        file_location=QFileDialog.getExistingDirectory(self,"Select Download Directory")#This Function Benfits not change name Video it's Still With it's name
        #::::::::this For Playlist Line Edit video :::::::::
        self.lineEdit_6.setText(file_location)
        #:::::this For Youtube Video Tab::::::::::::
        self.lineEdit_4.setText(file_location)


    #::::::::::::::::this Function make To Download File after choose propereties of video::::::::::::::::
    def Download_from_Youtube(self):
        video_link=self.lineEdit_3.text()
        Video_Function=pafy.new(video_link)
        save_file=self.lineEdit_4.text()
        stream=Video_Function.allstreams

        quality=self.comboBox.currentIndex()
        try:
            Download=stream[quality].download(filepath=save_file)
            QMessageBox.information(self,"Finshed Video","The Video Download Finished")
        except Exception :
            QMessageBox.warning(self,"download Faild","the Video Donwload Failed!!")
    
    #:::::::::::::::::::::::This Function We make it To Download More video in One Moment or PlayList::::::::::::::::::::::
    def PlayList_Videos(self):
        playList_Url=self.lineEdit_5.text()
        save_location_playlist=self.lineEdit_6.text()
        playlist_pafy=pafy.get_playlist(playList_Url)
        videos=playlist_pafy['items']
        os.chdir(save_location_playlist)

        if os.path.exists(str(playlist_pafy['title'])):
           os.chdir(str(playlist_pafy['title']))
        # os.chdir(save_loaction_playlist)
        else:
            os.mkdir(str(playlist_pafy['title']))
            os.chdir(str(playlist_pafy['title']))

        for video in videos:
            p=video['pafy']
            # print(p)
            Get_Best=p.getbest(perftype="mp4")
            Get_Best.download()


def Main_Window():
    #we will define App variable To Program::
    App=QApplication(sys.argv)
    #define ::Window:: Variable To Put in it The Main Class Name 
    Window=MainApp()
    
    Window.show()
    #this command it help program to wont stop Until the User Want::
    App.exec_()



if __name__=='__main__':
    Main_Window()

