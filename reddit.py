import json
import praw
import requests
import requests.auth
from secrets import Reddit

class RedditClient:

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=Reddit.clientId,
            client_secret=Reddit.clientSecret,
            password=Reddit.password,
            user_agent=Reddit.UserAgent,
            username=Reddit.username
        )
        self.reddit.read_only = True

    def getSubreddit(self, subredditName):
        self.subreddit = self.reddit.subreddit(subredditName)

    def getPosts(self, type, limit):
        if type=="hot":
            return self.subreddit.hot(limit=limit)
        elif type=="controversial":
            return self.subreddit.controversial(limit=limit)
        elif type=="new":
            return self.subreddit.new(limit=limit)
        elif type=="rising":
            return self.subreddit.rising(limit=limit)
        elif type=="top":
            return self.subreddit.top(limit=limit)
        else:
            raise Exception

    def getRedditorData(self, name):
        redditor = self.reddit.redditor(name)

        try:
            count = 0
            scoreSum = 0
            commentSum = 0

            for submission in redditor.submissions.new(limit = 1000):
                commentSum += submission.num_comments
                scoreSum += submission.score
                count += 1

            mean_score = scoreSum / count
            mean_comments = commentSum / count

            return {
                "name": redditor.name,
                "id": redditor.id,
                "posts_count": count,
                "posts_mean_score": '{:.2f}'.format(mean_score),
                "posts_mean_num_comments": '{:.2f}'.format(mean_comments)
            }
        except Exception as e:
            print(e)
            print(name)
            return {
                "name": name
            }


if __name__ == '__main__':
    redditClient = RedditClient()
    redditClient.getSubreddit("memes")
    memes = redditClient.getPosts("hot", 3)
    memesArr = []
    for meme in memes:
        m = {
            "author": meme.author,
            "title": meme.title,
            "id": meme.id,
            "comments": meme.num_comments,
            "permalink": meme.permalink,
            "score": meme.score,
            "created": meme.created_utc,
            "text": meme.selftext,
            "url": meme.url
        }
        memesArr.append(m)
    print(memesArr)
    print(redditClient.getRedditorData("spez"))