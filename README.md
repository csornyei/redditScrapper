# Reddit Scrapper

This project was made to get reddit posts and save them to MongoDB for later use.
I used it in a University assignment about ***Memes getting popular on Reddit***

## Usage

1. Install the requirements
2. Create a secrets.py based on the secrets.pub.py
3. To save data in MongoDB run `python main.py`
4. To download the images from the saved posts run `python getImage.py`, it will save the images to the *Images* folder


## TODO

- [x] Move image download logic to main.py
- [x] Run command based on arguments
- [x] Set subreddit, post type with arguments
- [x] Image download parameters with arguments
- [ ] Create CSV export logic
