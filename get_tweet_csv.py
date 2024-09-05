import json
import csv
import argparse
import os
from datetime import datetime


# Default arguments
default_input_filename = "input/tweets.json"
default_ouput_filename = "output/tweet_info.csv"

# Constants
tweet_date_format = "%a %b %d %H:%M:%S %z %Y"
tweet_https = "https://twitter.com/whatever/status/"


def verify_directory(output_filename):
    output_directory = os.path.dirname(output_filename)

    if output_directory != '' and not os.path.exists(output_directory):
        os.makedirs(output_directory)

    return


def extract_tweet_info(tweet):
    tweet_id = tweet["id_str"]
    tweet_date = tweet["created_at"]
    tweet_text = f"{tweet["full_text"].replace("\n", " ")},"

    parsed_date = datetime.strptime(tweet["created_at"], tweet_date_format)
    tweet_iso_date = parsed_date.astimezone().isoformat()
    tweet_unix_timestamp = parsed_date.timestamp()

    has_media = "extended_entities" in tweet and "media" in tweet["extended_entities"]
    possible_rt = tweet["full_text"].startswith("RT @") if tweet["full_text"] is not None else False
    tweet_url = tweet_https + tweet_id

    return {
        "tweet_id": tweet_id,
        "tweet_date": tweet_date,
        "tweet_iso_date": tweet_iso_date,
        "tweet_unix_timestamp": tweet_unix_timestamp,
        "has_media": has_media,
        "possible_rt": possible_rt,
        "tweet_text": tweet_text,
        "tweet_url": tweet_url,
    }


def main():
    parser = argparse.ArgumentParser(description="Extract important tweet information from a Twitter archive JSON file.")
    parser.add_argument(
        "--input_filename",
        type=str,
        help="The input JSON file containing the Twitter archive.",
        default=default_input_filename,
    )
    parser.add_argument(
        "--output_filename",
        type=str,
        help="The output CSV file containing all info of the tweets.",
        default=default_ouput_filename,
    )

    args = parser.parse_args()

    input_filename = args.input_filename
    output_filename = args.output_filename

    verify_directory(output_filename)

    data = []

    try:
        with open(input_filename, "r", encoding="utf-8") as file:
            data = json.load(file)

    except Exception as e:
        print(f"An error occurred when trying to open input file {input_filename}: {e}")
        return 1

    all_tweet_info = []

    for tweet_data in data:
        tweet = tweet_data.get("tweet", {})
        tweet_info = extract_tweet_info(tweet)
        all_tweet_info.append(tweet_info)

    all_tweet_info.sort(key=lambda tweet: tweet["tweet_unix_timestamp"])

    try:
        with open(output_filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "tweet_id",
                "tweet_date",
                "tweet_iso_date",
                "tweet_unix_timestamp",
                "has_media",
                "possible_rt",
                "tweet_text",
                "tweet_url",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for info in all_tweet_info:
                writer.writerow(info)

    except Exception as e:
        print(f"An error ocurred when trying to write to ouput file {output_filename}: {e}")
        return 1

    print(f"Process finished (number of tweets extracted: {len(all_tweet_info)}). Check out your file at {output_filename}!")

    return 0


if __name__ == "__main__":
    main()
