from dbInsert import handleMeme, setSubreddit
from getImage import getMemesFromDB, filterMemesWithoutUrl, downloadMemeImage
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
    for meme in filteredMemes:
        downloadMemeImage(meme)

elif args.csv:
    print("I will export the database to CSV!")
