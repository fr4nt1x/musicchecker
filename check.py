from mutagen.easyid3 import EasyID3
from models import File, Folder
from init import session
import os
from datetime import date
root = os.path.join('F:',os.sep,r'Musik')

resultfiles = []
resultfolders = []

def checkDirs(dirs,parentFolder):
    names =[x.name for x in parentFolder.folders]        
    allDirsFound = []       
    if not set(names) == set(dirs):
        print("directories: ", set(names) - set(allDirsFound) ," missing in: " + parentFolder.name)
        print("directories: ",  set(allDirsFound) - set(names) ," extra in: " + parentFolder.name)
        
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
                

            tracknumber = -1
            artist = -1
            titlestring = -1
            
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

            if not dataBaseFile.title == titlestring:
                resultfiles.append(f + " titlestring missing.")
                    
            elif not dataBaseFile.artist == artist:
                resultfiles.append(f + " artist missing.")
                    
            elif not dataBaseFile.trackNumber == tracknumber:
                resultfiles.append(f+ " tracknumber missing")
           
                
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
                    
            
print("Files with changed id3 tags: " + ",".join(resultfiles))
print("Directories not found: " + ",".join(resultfolders))
