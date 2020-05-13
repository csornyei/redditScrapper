
from time import sleep
from reddit import RedditClient
from mongo import MongoDB
from datetime import datetime

LIMIT = 1000

def getMemes(type):
    memesArr = []
    memes = rc.getPosts(type, LIMIT)
    for meme in memes:
        try:
            m = {
                "type": type,
                "author": meme.author.name,
                "title": meme.title,
                "id": meme.id,
                "comments": [
                    {time: meme.num_comments}
                ],
                "permalink": meme.permalink,
                "score": [
                    {time: meme.score}
                ],
                "created": meme.created_utc,
                "text": meme.selftext,
                "url": meme.url,
                "upvotes": meme.score,
                "num_comments": meme.num_comments,
                "type_history": [
                    {time: type}
                ]
            }
            memesArr.append(m)
        except:
           print(meme)
    return memesArr

def insertMemeToDB(localMeme, type):
    filt = {
        "author": localMeme["author"],
        "title": localMeme["title"],
        "created": localMeme["created"],
        "id": localMeme["id"]
    }
    if mongodb.findMeme(filt) is None:
        mongodb.writeData(localMeme)
        print("Inserted")
    else:
        update = {
            "$push": {
                "score": {time: localMeme["upvotes"]},
                "comments": {time: localMeme["num_comments"]},
                "type_history": {time: type}
            },
            "$set": {
                "upvotes": localMeme["upvotes"],
                "num_comments": localMeme["num_comments"]
            }
        }
        mongodb.findMemeAndUpdate(filt, update)
        print("Updated")

time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
rc = RedditClient()
mongodb = MongoDB()
rc.getSubreddit("memes")
hotMemes = getMemes("hot")
newMemes = getMemes("new")
index = 0
print("HOT")
for meme in hotMemes:
    insertMemeToDB(meme, "hot")
    index = index + 1
    if index % 50 == 0:
        print(f"{index} of {len(hotMemes)}")
    sleep(0.5)

index = 0
print("HOT")
for meme in newMemes:
    insertMemeToDB(meme, "new")
    index = index + 1
    if index % 50 == 0:
        print(f"{index} of {len(newMemes)}")
    sleep(0.5)