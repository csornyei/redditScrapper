from os import path
from datetime import datetime
from csv import DictWriter
from dbInsert import handleMeme, setSubreddit
from getImage import getMemesFromDB, filterMemesWithoutUrl, downloadMemeImage
from csvExport import writeMemesToCSV
from arguments import args

print(args)

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

elif args.csv:
    print("I will export the database to CSV!")
    try:
        limit = int(args.limit)
    except:
        limit = 0
    writeMemesToCSV(limit)
