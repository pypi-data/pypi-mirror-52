# Reddit Comment Cloud

Python3.7+ wrapper for generating word clouds from a Reddit user's comments.

![Reddit Comment Cloud for /u/SuddenlySnowden](SuddenlySnowden.png)

## Built upon
+ [PRAW](https://github.com/praw-dev/praw) (Python Reddit API Wrapper)
+ [WordCloud](https://github.com/amueller/word_cloud)
+ matplotlib

## Use
This example will render the WordCloud of /u/SuddenlySnowden and save the image under _SuddenlySnowden.png_ in the current working directory.

```
from redditcommentcloud import CommentCloud
cc = CommentCloud()
cc.renderWordCloud(username='SuddenlySnowden')
```


## Install
The code was written for Python3.7+.

__Optionally__: Create a Python virtual environment:
```
python -m venv .venv
source .venv/bin/activate
```
Type `deactivate` when you are done

__Clone this repository__ or install it using `pip install redditcommentcloud`.

__Installing the dependencies__
```
pip install -r requirements.txt
```

__Supply Reddit API credentials__
This tool requires API credentials for the Reddit API.
Go to https://www.reddit.com/prefs/apps/, create an app and copy the keys.

Copy `redditcommentcloud/config.py.template` to `redditcommentcloud/config.py` and fill in the details.
Freely choose a presumably unique User-Agent for the bot.
