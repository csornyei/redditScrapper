from time import sleep
from reddit import RedditClient
from mongo import MongoDB
from datetime import datetime

mongodb = MongoDB()
rc = RedditClient()
time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

LIMIT = 1000

def setSubreddit(subredditName):
    print(f"Setting subreddit to {subredditName}")
    rc.getSubreddit(subredditName)

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

def handleMeme(type):
    print(f"Starting {type}\n")
    memes = getMemes(type)
    index = 0
    for meme in memes:
        index += 1
        insertMemeToDB(meme, type)
        print(f"{index} of {len(memes)}", end="\r", flush=True)
        sleep(0.5)
    print(f"{type} is done!")
