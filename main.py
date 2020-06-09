from os import path
from time import sleep
from csv import DictWriter
from arguments import args
from datetime import datetime
from csvExport import writeMemesToCSV, writeUsersToCSV
from dbInsert import handleMeme, setSubreddit, insertUser
from getImage import getMemesFromDB, filterMemesWithoutUrl, downloadMemeImage

if args.insert:
    setSubreddit(args.sub)
    if args.hot:
        handleMeme("hot")
    if args.new:
        handleMeme("new")
    if not(args.hot) and not(args.new):
        handleMeme("hot")
        handleMeme("new")

elif args.download:
    print("I will download all the images!")
    try:
        limit = int(args.limit)
    except:
        limit = 0
    memeCursor = getMemesFromDB(limit)
    filteredMemes = filterMemesWithoutUrl(memeCursor)
    with open(path.join(path.dirname(__file__), "csv", f"images-{datetime.now().strftime('%y-%m-%d-%H-%M-%S')}.csv"), "w") as file:
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
            memeCounter += 1

elif args.csv:
    if args.user:
        print("I will export user data to CSV!")
        writeUsersToCSV()
    else:
        print("I will export post data to CSV!")
        try:
            limit = int(args.limit)
        except:
            limit = 0
        writeMemesToCSV(limit)

elif args.user:
    if args.name != 0:
        insertUser(args.name)
    elif args.file != 0:
        count = 0
        with open(args.file) as file:
            for line in file:
                insertUser(line.strip())
                count += 1
                if count % 100 == 0:
                    print(count)
    else:
        print("You didn't provided name or file!")