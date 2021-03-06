from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from models import File, Folder
from init import session
import os
from datetime import date
root = os.path.join('I:',os.sep,r'Musik')
ShowBitrate = False
BitrateLowerBound = 190000
resultfiles = []
resultfolders = []

def checkDirs(dirs,parentFolder):
    names =[x.name for x in parentFolder.folders]        
    allDirsFound = []       
    if not set(names) == set(dirs):
        print("directories: ", set(names) - set(dirs) ," missing in: " + parentFolder.name)
        print("directories: ",  set(dirs) - set(names) ," extra in: " + parentFolder.name)
        
def checkFiles(files, parentFolder,rootPath):
    dataBaseFiles = parentFolder.files
    allFilesFound = []
    dataBaseFilesNames =[x.name for x in dataBaseFiles]
    for f in files:
        if f.split('.')[-1] == 'mp3':
            size=os.path.getsize(os.path.join(rootPath,f))
            try:
                id3 = EasyID3(os.path.join(rootPath,f))
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
                if not artist==-1:
                    if 'albumartist' in id3:
                        artist = id3['albumartist'][0]
                if 'title' in id3:
                    titlestring = id3['title'][0]    
            else:
                print(rootPath+f+" has no id3 tag.")
                

            if f in dataBaseFilesNames:
                dataBaseFile = dataBaseFiles[dataBaseFilesNames.index(f)]
                
            if not dataBaseFile.title == str(titlestring):
                resultfiles.append(rootPath + os.sep + f + " titlestring has changed.")
                    
            elif not dataBaseFile.artist == str(artist):
                resultfiles.append(rootPath + os.sep + f + " artist has changed.")
                    
            elif not dataBaseFile.trackNumber == tracknumber:
                resultfiles.append(rootPath + os.sep + f + " tracknumber has changed.")

            elif not dataBaseFile.bitrate == bitrate:
                resultfiles.append(rootPath + os.sep + f + " bitrate has changed.")
                
            if titlestring == -1 or artist== -1 or tracknumber == -1 :
                print(rootPath + os.sep + f + " has missing id3 entries.")
            
            if ShowBitrate and bitrate <= BitrateLowerBound:
                print(rootPath + os.sep+ f+ " has a bitrate of: "+ str(bitrate)+"." )
            allFilesFound.append(f)
            
    if not set(dataBaseFilesNames) == set(allFilesFound):
        print("Files: ", set(dataBaseFilesNames) - set(allFilesFound) ," missing in: " + parentFolder.name)
        print("Files: ", set(allFilesFound)- set(dataBaseFilesNames) ," extra in: " + parentFolder.name)


for r,dirs,files in os.walk(root):
    parentFolderList = r.split(os.sep)
    parentFolderList = parentFolderList[len(root.split(os.sep)):]
    parentFolderList.insert(0,"Root")
    path = "/".join(parentFolderList)
    
    parentFolder = session.query(Folder).filter_by(pathToFolder = path).first()

    if parentFolder == None:
        resultfolders.append(r)
        break
    else:
        checkDirs(dirs, parentFolder)
        checkFiles(files,parentFolder, r)
                    
            
print("Files with changed id3 tags: " + "\n".join(resultfiles))
