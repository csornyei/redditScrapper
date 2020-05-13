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

if __name__ == '__main__':
    mongodb = MongoDB()
    allTheMemes = mongodb.getAllMeme(limit = 15)
    for doc in allTheMemes:
        if doc["url"] != "":
            author = doc["author"]
            currentTime = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
            _, extension = os.path.splitext(doc["url"])
            if extension != "":
                currentDir = os.path.dirname(__file__)
                filename = os.path.join(currentDir, "images", f"{author}-{currentTime}{extension}")
                downloadImage(doc["url"], filename)