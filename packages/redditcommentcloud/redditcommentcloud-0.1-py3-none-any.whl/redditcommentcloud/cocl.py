from .config import REDDIT_USER_AGENT, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET
import praw
from wordcloud import WordCloud
import matplotlib.pyplot as plt


class CommentCloud(object):
    def __init__(self):
        self.reddit = praw.Reddit(user_agent=REDDIT_USER_AGENT,
                                  client_id=REDDIT_CLIENT_ID,
                                  client_secret=REDDIT_CLIENT_SECRET)

    def renderWordCloud(self, username):
        text = ""
        for comment in self.reddit.redditor(name=username).comments.new(limit=None):
            text += comment.body.lower()
        wordcloud = WordCloud(width=1280, height=720, margin=0, prefer_horizontal=0.8).generate(text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(username+'.png', dpi=200, bbox_inches='tight', pad_inches = 0)


if __name__ == '__main__':
    pass
