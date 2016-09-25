from mutagen.easyid3 import EasyID3
from models import Title, ID3
from init import session
import os
from datetime import date

allTitles = session.query(Title).all()

root = os.path.join('F:',os.sep,r'Musik')
changed = []

for r,dirs,files in os.walk(root):

    for f in files:
        if f.split('.')[-1] == 'mp3':
            try:
                index = [x.name for x in allTitles].index(f)

            except ValueError:
                index = "NotFound"
            if index == "NotFound" :
                changed.append(("NotFound",os.path.join(root,r,f)))
                continue
            
            currentTitle = allTitles[index]
            
    #add path check
            
            size=os.path.getsize(os.path.join(r,f))
            if currentTitle.fileSize != size:
                print(size-currentTitle.fileSize)
                changed.append(("Size",os.path.join(root,r,f)))
                continue
            
            try:
                id3 = EasyID3(os.path.join(r,f))
            except:
                id3 = -1
                
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

                if titlestring !=currentTitle.id3tag.name :
                    changed.append(("title",os.path.join(root,r,f)))
                    continue
                elif tracknumber !=currentTitle.id3tag.trackNumber :
                    changed.append(("track",os.path.join(root,r,f)))
                    continue
                elif artist !=currentTitle.id3tag.artist :
                    changed.append(("artist",os.path.join(root,r,f)))
                    continue

print(changed)
