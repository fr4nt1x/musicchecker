from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from models import File, Folder
from init import session
import os
from datetime import date

root = os.path.join('G:',os.sep,r'Musik')
folder = session.query(Folder).filter_by(pathToFolder = "Root").first()

if folder ==None:
    session.add(Folder(name = "Root", pathToFolder ="Root"))
    session.commit()

for r,dirs,files in os.walk(root):
    parentFolderList = r.split(os.sep)
    parentFolderList = parentFolderList[len(root.split(os.sep)):]
    parentFolderList.insert(0,"Root")
    path = "/".join(parentFolderList)
        
    parentFolder = session.query(Folder).filter_by(pathToFolder = path).first()
    for d in dirs:
        folder = Folder(name = d, parent = parentFolder,pathToFolder = "/".join([path,d]))
    
    

    for f in files:
        if f.split('.')[-1] == 'mp3':
            size=os.path.getsize(os.path.join(r,f))
            try:
                id3 = EasyID3(os.path.join(r,f))
            except:
                id3 = -1
            try:
                mptest = MP3(os.path.join(r,f))
            except:
                mptest = -1
                
            bitrate = 0
            tracknumber = -1
            artist = -1
            titlestring = -1
            if mptest != -1:
                bitrate = mptest.info.bitrate
                
            if id3 != -1:
                if 'tracknumber' in id3:
                    try:
                        tracknumber = int(id3['tracknumber'][0])
                    except:
                        tracknumber = -2
                if 'artist' in id3 :
                    artist = id3['artist'][0]
                if not artist == -1:
                    if 'albumartist' in id3:
                        artist = id3['albumartist'][0]
                if 'title' in id3:
                    titlestring = id3['title'][0]
                    
                
            file = File(name = f, parent = parentFolder, dateLastChanged =date.today() , bitrate= bitrate,artist=artist , trackNumber = tracknumber , title = titlestring )
            session.add(file)

session.commit()         
