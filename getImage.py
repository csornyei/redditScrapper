import os
import requests
import shutil
from csv import DictWriter
from mongo import getMemesFromDB
from datetime import datetime

def downloadImage(imageUrl, imageName):
    r = requests.get(imageUrl, stream = True)

    if r.status_code == 200:
        r.raw.decode_content = True

        with open(imageName, 'wb') as file:
            shutil.copyfileobj(r.raw, file)
        return True
    else:
        return False

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
    if downloadImage(url, fileName):
        return fileName
    else:
        return "No image downloaded"


if __name__ == '__main__':
    memes = getMemesFromDB(15)
    filteredMemes = filterMemesWithoutUrl(memes)
    with open(os.path.join(os.path.dirname(__file__), "csv", f"images-{datetime.now().strftime('%y-%m-%d-%H-%M-%S')}.csv"), "w") as file:
        fieldnames = ["id", "title", "author", "filename"]
        writer = DictWriter(file, fieldnames)
        writer.writeheader()
        for meme in filteredMemes:
            filename = downloadMemeImage(meme)
            row = {
                "id": meme["id"],
                "title": meme["title"],
                "author": meme["author"],
                "filename": filename
            }
            writer.writerow(row)
