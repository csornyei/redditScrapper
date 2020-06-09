import os
from csv import DictWriter
from datetime import datetime
from mongo import getMemesFromDB, getUsersFromDB

def getDataFromCursor(cursor):
    datas = []
    for data in cursor:
        datas.append(data)
    return datas

def getCSVFileName(type):
    currentDir = os.path.dirname(__file__)
    currentTime = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    return os.path.join(currentDir, "csv", f"{type}-{currentTime}.csv")

def getCreatedDate(created_timestamp):
    try:
        date = datetime.fromtimestamp(created_timestamp)
        return date.strftime("%Y/%m/%d %H:%M:%S")
    except:
        return created_timestamp

def getChangedToHot(meme):
    if meme["type"] == "hot":
        return 1
    else:
        changed = 0
        try:
            for hist in meme["type_history"]:
                histKey = [*hist][0]
                if hist[histKey] == "hot":
                    changed = histKey
            return changed
        except KeyError:
            return 0

def getWriteableMeme(meme):
    first_comments = -100
    max_comments = 0
    first_appeared = 0
    last_appeared = 0

    for comm in meme["comments"]:
        commentTimeStamp = [*comm][0]
        last_appeared = commentTimeStamp
        if first_appeared == 0:
            first_appeared = commentTimeStamp
        if first_comments == -100:
            first_comments = comm[commentTimeStamp]
        if max_comments < comm[commentTimeStamp]:
            max_comments = comm[commentTimeStamp]

    first_score = -100
    max_score = 0
    for score in meme["score"]:
        scoreTimeStamp = [*score][0]
        if first_score == -100:
            first_score = score[scoreTimeStamp]
        if max_score < score[scoreTimeStamp]:
            max_score = score[scoreTimeStamp]

    return {
        "id": meme["id"],
        'type': meme["type"],
        'author': meme["author"],
        'title': meme["title"],
        'created': getCreatedDate(meme["created"]),
        'transcript': "",
        'max_score': max_score,
        'score_change': max_score - first_score,
        'max_comments': max_comments,
        'comment_change': max_comments - first_comments,
        'changed_to_hot': getChangedToHot(meme),
        'categories': "",
        'first_appeared': first_appeared,
        'last_appeared': last_appeared,
    }

def writeMemesToCSV(limit):
    memeCursor = getMemesFromDB(limit)
    memes = getDataFromCursor(memeCursor)

    with open(getCSVFileName("post"), mode="w") as file:
        fieldnames = ['id', 'type', 'author', 'title', 'created', 'transcript', 'max_score', 'score_change', 'max_comments', 'comment_change', 'changed-to-hot', 'categories']
        writer = DictWriter(file, fieldnames)
        writer.writeheader()
        for meme in memes:
            writer.writerow(getWriteableMeme(meme))

def writeUsersToCSV():
    userCursor = getUsersFromDB()
    users = getDataFromCursor(userCursor)

    with open(getCSVFileName("users"), mode="w") as file:
        fieldnames = ['name', 'id', 'posts_count', 'posts_mean_score', 'posts_mean_num_comments', '_id', 'timestamp']
        writer = DictWriter(file, fieldnames)
        writer.writeheader()
        for user in users:
            writer.writerow(user)


if __name__ == '__main__':
    writeMemesToCSV(15)