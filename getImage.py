import os
import requests
import shutil
from mongo import MongoDB
from datetime import datetime

def downloadImage(imageUrl, imageName):
    r = requests.get(imageUrl, stream = True)

    if r.status_code == 200:
        r.raw.decode_content = True

        with open(imageName, 'wb') as file:
            shutil.copyfileobj(r.raw, file)
        print("Image downloaded!")
    else:
        print("Can't download image!")
        print(imageUrl)

# if limit is 0 it will get everything
def getMemesFromDB(limit):
    mongodb = MongoDB()
    return mongodb.getAllMeme(limit = limit)

def getFileExtensionFromUrl(url):
    _, extension = os.path.splitext(url)
    return extension

def filterMemesWithoutUrl(memesCursor):
    memes = []
    for meme in memesCursor:
        if meme["url"] != "":
            extension = getFileExtensionFromUrl(meme["url"])
            if extension != "":
                memes.append(meme)
    return memes

def getFileName(author, extension):
    currentDir = os.path.dirname(__file__)
    currentTime = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    return os.path.join(currentDir, "images", f"{author}-{currentTime}{extension}")

def downloadMemeImage(meme):
    url = meme["url"]
    fileName = getFileName(meme["author"], getFileExtensionFromUrl(url))
    downloadImage(url, fileName)


if __name__ == '__main__':
    memes = getMemesFromDB(0)
    filteredMemes = filterMemesWithoutUrl(memes)
    for meme in filteredMemes:
        downloadMemeImage(meme)
