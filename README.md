# EATM

Acronym for ~~*eat meat*~~ *Extract Archive Tweet Media*. It's a set of Python scripts to extract basic information about your tweets from your archive.

## Features

* Summarize your tweet database into a CSV file
* Download all the tweet media you have tweeted/retweeted/replied

## Requirements

* Python 3.10
* Modules in `requirements.txt` (version may vary though)
* Experience using terminal/console

## First steps

### Twitter Archive

First of, you must request your [Twitter Archive](https://help.x.com/en/managing-your-account/accessing-your-x-data#:~:text=Where%20can%20I%20find%20my%20X%20data%3F), which will be sent to you once it's finished (time varies depending on the amount of data you have).

### Extracting tweets

You will soon notice there are three elements inside this archive file.

```text
    Your Twitter Archive
(1) │   Your archive.html
(2) ├───assets
(3) └───data
        │   account-creation-ip.js
        │   ...
(>)     │   tweets.js
        │   ...
        │   verified.js
        │   
        ├───community_tweet_media
        ├─── - - -
        └───tweets_media
```

Go inside the `data` folder, and copy the `tweets.js` file, since is the only one you'll need to use this script.

### Format file

Despite the extension, this file could be easily "converted" to a JSON file. Consider the file to have a similar structure as the following.

```js
window.YTD.tweets.part0 = [
  {
    "tweet" : {
        ...
    }
  },
]
```

You only have to **delete the first part of the line** (the one with `window.YTD`). After doing so, the result should be like the one below.

```js
[
  {
    "tweet" : {
        ...
    }
  },
]
```

Finally, change the extension from `.js` to `.json`, and then it's ready to go!

## Commands

Assuming you've already [installed Python](https://www.python.org/downloads/), [configured a *venv*](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/), and installed the `requirements.txt` modules, you can run any of the following three scripts.

**Tip.** Whenever you are unsure how to run the commands, `-h` option will be your friend!

### `get_tweet_csv.py`

This script will collect very basic stuff, like `tweet_id`, `tweet_date`, `tweet_text` and `tweet_url` (among others).

The complete command is the following:

```sh
py get_tweet_csv.py --input_filename <input_filename> --output_filename <output_filename>
```

All argument default options are the following:

| Argument | Default value | Description |
| - | - | - |
| `input_filename` | input/tweets.json | The input JSON file containing the Twitter archive. |
| `output_filename` | output/tweet_info.csv | The output CSV file containing all info of the tweets. |

### `get_media_csv.py`

This script is similar to the previous one. However, this one is specialized in getting tweet's media ONLY. Contains data like `tweet_id`, `tweet_date`, `tweet_url`, `media_id`, `media_type`, `media_url`, etc.

Its arguments are basically the same as the previous command. So the complete command is the following:

```sh
py get_media_csv.py --input_filename <input_filename> --output_filename  <output_filename>
```

All argument default options are the following:

| Argument | Default value | Description |
| - | - | - |
| `input_filename` | input/tweets.json | The input JSON file containing the Twitter archive. |
| `output_filename` | output/media_info.csv | The output CSV file containing the media information. |

**Note that this script won't download any media.**

### `download_media.py`

As you may deduce by the name, this script lets you download all type of media from these tweets/retweets/replies.

This script, however, requires an output file from `get_media_csv.py`. The complete command is the following:

```sh
py download_media.py --column_tweet_id <column_tweet_id> --column_tweet_unix_timestamp <column_tweet_unix_timestamp> --column_media_id <column_media_id> --column_media_url <column_media_url> --input_filename <input_filename> --output_directory <output_directory>
```

All argument default options are the following:

| Argument | Default value | Description |
| - | - | - |
| `column_tweet_id` | tweet_id | The column name where the Tweet ID is stored. |
| `column_tweet_unix_timestamp` | tweet_unix_timestamp | The column name where the Tweet UNIX timestamp is stored. |
| `column_media_id` | media_id | The column name where the media ID is stored. |
| `column_media_url` | media_url | The column name where the media URL is stored. |
| `input_filename` | output/media_info.csv | The input CSV file containing the Twitter media URLs. |
| `output_directory` | output/media/ | The ouput folder name which the media will be saved. |

Don't panic! If you are, indeed, using the `get_media_csv.py` script output, the basic usage often will be the following:

```sh
py download_media.py --input_filename <input_filename> --output_directory <output_directory>
```

Pretty neat, right?

## Tips

The result will contain tweets ordered by its UNIX timestamp ascendingly. However, you can also order them by its `tweet_id` column.

If you still insist on the UNIX timestamp, I recommend converting `tweet_unix_timestamp` by adding another column with the following formula (assuming its column is `D2`): `=D2/(24*60*60) + DATE(1970,1,1)`.

## Notes

If there's any error with the script or this README, let me know by opening an issue, or maybe just throw me a message at my Twitter profile!
