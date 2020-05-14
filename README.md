# Reddit Scrapper

This project was made to get reddit posts and save them to MongoDB for later use.
I used it in a University assignment about ***Memes getting popular on Reddit***

## Usage

1. Install the requirements
2. Create a secrets.py based on the secrets.pub.py
3. Run `python main.py` with the following arguments:
   1. `--insert` to scrape reddit and store them in MongoDB
      - This case you can set `-s`, `--hot` and `--new` arguments
   2. `--download` to download images stored in MongoDB
      - With the `--limit` argument you can set how many images will be downloaded
   3. `--csv` to export the database content into a CSV file


## TODO

- [x] Move image download logic to main.py
- [x] Run command based on arguments
- [x] Set subreddit, post type with arguments
- [x] Image download parameters with arguments
- [ ] Create CSV export logic
