import argparse

parser = argparse.ArgumentParser(description="Scrapping reddit for data")

parser.add_argument('-i', '--insert', action="store_true", help="Insert mode: get reddit posts and store them in MongoDB")
parser.add_argument('--loop', action="store_true", help="If set the script will run every two hours")
parser.add_argument('-s', '--sub', action="store", default="memes", help="Which subreddit should the program scrape (default: memes)")
parser.add_argument('--hot', action="store_true", help="Set to download the hot posts, if neither hot nor new is set, it will do both")
parser.add_argument('--new', action="store_true", help="Set to download the new posts, if neither hot nor new is set, it will do both")

parser.add_argument('-d', '--download', action="store_true", help="Download: download the images stored in MongoDB")
parser.add_argument('-l', '--limit', action="store", default=0, help="How many posts should the program process? Available both for download and CSV export (default: all)")

parser.add_argument('-c', '--csv', action="store_true", help="CSV Export: export the stored posts to CSV")


args = parser.parse_args()