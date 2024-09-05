import argparse
import pandas as pd
import requests
import os
from urllib.parse import urlparse, unquote
from datetime import datetime


# Default arguments
default_column_tweet_id = "tweet_id"
default_column_tweet_unix_timestamp = "tweet_unix_timestamp"
default_column_media_id = "media_id"
default_column_media_url = "media_url"
default_input_filename = "output/media_info.csv"
default_output_directory = "output/media/"

# Constants
custom_date_format = "%Y-%m-%d_%H.%M.%S"


def verify_directory(output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    return


def get_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    return unquote(filename)


def get_media_format(filename):
    *_, extension = filename.split(".")

    return extension


def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(description='Download media files from the generated Twitter media file.')
    parser.add_argument(
        '--column_tweet_id',
        type=str,
        help='The column name where the Tweet ID is stored.',
        default=default_column_tweet_id
    )
    parser.add_argument(
        '--column_tweet_unix_timestamp',
        type=str,
        help='The column name where the Tweet UNIX timestamp is stored.',
        default=default_column_tweet_unix_timestamp
    )
    parser.add_argument(
        '--column_media_id',
        type=str,
        help='The column name where the media ID is stored.',
        default=default_column_media_id
    )
    parser.add_argument(
        '--column_media_url',
        type=str,
        help='The column name where the media URL is stored.',
        default=default_column_media_url
    )
    parser.add_argument(
        '--input_filename',
        type=str,
        help='The input CSV file containing the Twitter media URLs.',
        default=default_input_filename
    )
    parser.add_argument(
        '--output_directory',
        type=str,
        help='The ouput folder name which the media will be saved.',
        default=default_output_directory
    )

    args = parser.parse_args()

    column_tweet_id = args.column_tweet_id
    column_tweet_unix_timestamp = args.column_tweet_unix_timestamp
    column_media_id = args.column_media_id
    column_media_url = args.column_media_url
    csv_media_file = args.input_filename
    output_directory = args.output_directory
    
    verify_directory(output_directory)

    dataframe = pd.read_csv(csv_media_file)

    successful_downloads = 0
    for index, row in dataframe.iterrows():
        tweet_id = row[column_tweet_id]
        tweet_unix_timestamp = row[column_tweet_unix_timestamp]
        media_id = row[column_media_id]
        media_url = row[column_media_url]

        parsed_date = datetime.fromtimestamp(tweet_unix_timestamp)
        tweet_formatted_date = parsed_date.strftime(custom_date_format)

        actual_filename = get_filename_from_url(media_url)
        extension = get_media_format(actual_filename)

        filename = f"{tweet_id} {media_id} {tweet_formatted_date}.{extension}"
        save_path = os.path.join(output_directory, filename)

        if download_file(media_url, save_path):
            print(f"[{tweet_id}][{index}/{len(dataframe)}] Media {media_id} downloaded correctly: " + filename)
            successful_downloads += 1
        else:
            print(f"[{tweet_id}][{index}/{len(dataframe)}] Couldn't download {media_id}...")

    print(f"Process finished. (number of media files extracted: {successful_downloads}). Check out your files at {output_directory}!")

    return 0


if __name__ == '__main__':
    main()
