import json
import csv
import argparse
import os
from datetime import datetime


# Default arguments
default_input_filename = "input/tweets.json"
default_ouput_filename = "output/media_info.csv"

# Constants
tweet_date_format = "%a %b %d %H:%M:%S %z %Y"
tweet_https = "https://twitter.com/whatever/status/"


def verify_directory(output_filename):
    output_directory = os.path.dirname(output_filename)

    if output_directory != '' and not os.path.exists(output_directory):
        os.makedirs(output_directory)

    return


def extract_media_info(tweet):
    media_info = []

    if 'extended_entities' in tweet and 'media' in tweet['extended_entities']:
        tweet_id = tweet['id_str']
        tweet_date = tweet['created_at']
        
        parsed_date = datetime.strptime(tweet['created_at'], tweet_date_format)
        tweet_iso_date = parsed_date.astimezone().isoformat()
        tweet_unix_timestamp = parsed_date.timestamp()

        possible_rt = tweet['full_text'].startswith("RT @") if tweet['full_text'] is not None else False
        tweet_url = tweet_https + tweet_id

        for media in tweet['extended_entities']['media']:
            media_id = media['id_str']
            media_type = media['type']
            media_expanded_url = media['expanded_url']
            media_url = None
            error = None

            try:
                if media_type == 'photo':
                    media_url = f"{media['media_url_https']}?name=large"
                elif media_type in ['video', 'animated_gif']:
                    variants = media['video_info']['variants']
                    best_variant = max(variants, key=lambda v: int(v.get('bitrate', '0')))
                    media_url = best_variant['url']
                else:
                    media_url = None

            except Exception as e:
                error = str(e)

            media_info.append({
                'tweet_id': tweet_id,
                'tweet_date': tweet_date,
                'tweet_iso_date': tweet_iso_date,
                'tweet_unix_timestamp': tweet_unix_timestamp,
                'tweet_url': tweet_url,
                'possible_rt': possible_rt,
                'media_id': media_id,
                'media_type': media_type,
                'media_url': media_url,
                'media_expanded_url': media_expanded_url,
                'error': error
            })
            
    return media_info


def main():
    parser = argparse.ArgumentParser(description='Extract media URLs from a Twitter archive JSON file.')
    parser.add_argument(
        '--input_filename',
        type=str,
        help='The input JSON file containing the Twitter archive.',
        default=default_input_filename
    )
    parser.add_argument(
        '--output_filename',
        type=str,
        help='The output CSV file containing the media information.',
        default=default_ouput_filename
    )

    args = parser.parse_args()

    input_filename = args.input_filename
    output_filename = args.output_filename

    verify_directory(output_filename)

    data = []

    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

    except Exception as e:
        print(f"An error occurred when trying to open input file {input_filename}: {e}")
        return 1

    all_media_info = []

    for tweet_data in data:
        tweet = tweet_data.get('tweet', {})
        media_info = extract_media_info(tweet)
        all_media_info.extend(media_info)

    all_media_info.sort(key=lambda media: media['tweet_unix_timestamp'])

    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'tweet_id',
                'tweet_date',
                'tweet_iso_date',
                'tweet_unix_timestamp',
                'tweet_url',
                'possible_rt',
                'media_id',
                'media_type',
                'media_url',
                "media_expanded_url",
                'error'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for info in all_media_info:
                writer.writerow(info)
            
    except Exception as e:
        print(f"An error ocurred when trying to write to ouput file {output_filename}: {e}")
        return 1
    
    print(f"Process finished (number of media files extracted: {len(all_media_info)}). Check out your file at {output_filename}!")
    
    return 0


if __name__ == '__main__':
    main()
