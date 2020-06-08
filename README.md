# Reddit Scrapper

This project was made to get reddit posts and save them to MongoDB for later use.
I used it in a University assignment about ***Memes getting popular on Reddit***

## Usage

1. Install the requirements
2. Create a secrets.py based on the secrets.pub.py
3. Run `python main.py` with the following arguments:
   - `--insert` to scrape reddit and store them in MongoDB
      - This case you can set `--loop`, `-s`, `--hot` and `--new` arguments
   - `--download` to download images stored in MongoDB
      - With the `--limit` argument you can set how many images will be downloaded
   - `--csv` to export the database content into a CSV file
      - With the `--limit` argument you can set how many rows should be in the CSV

## TODO

- [x] ~~Move image download logic to main.py~~
- [x] ~~Run command based on arguments~~
- [x] ~~Set subreddit, post type with arguments~~
- [x] ~~Image download parameters with arguments~~
- [x] ~~Create CSV export logic~~
- [ ] Getting user data
- [ ] Multi threaded image download