from mutagen.easyid3 import EasyID3
from models import Title, ID3
from init import session
import os
from datetime import date

root = os.path.join('F:',os.sep,r'Musik')

for r,dirs,files in os.walk(root):

    for f in files:
        if f.split('.')[-1] == 'mp3':
            size=os.path.getsize(os.path.join(r,f))
            try:
                id3 = EasyID3(os.path.join(r,f))
            except:
                id3 = -1
            title = Title(name = f,directoryFromRoot= r[len(root)+1:],fileSize = size, dateLastChanged =date.today())

            if id3 != -1:
                if 'tracknumber' in id3:
                    try:
                        tracknumber = int(id3['tracknumber'][0])
                    except:
                        tracknumber = -2
                else:
                    tracknumber = -1
                if 'artist' in id3 :
                    artist = id3['artist'][0]
                if not artist:
                    if 'albumartist' in id3:
                        artist = id3['albumartist'][0]
                if 'title' in id3:
                    titlestring = id3['title'][0]
                    
                print(artist)   
                print(titlestring)

                tag = ID3(name=titlestring,artist=artist,trackNumber = tracknumber,title = title)
                session.add(tag)
            session.add(title)

session.commit()
            
