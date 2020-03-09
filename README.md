# Video Crawler

This package is meant to ease crawling video sources: from retrieving relevant metadata, scraping links given your keywords, to downloading for your input datasets.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [To-Do](#to-do)
- [Support](#support)
- [Contributing](#contributing)

## Installation

This project is tested on Ubuntu 18.04 and run with Python 3.6.9. Preferably use a virtualenv [Instructions to install and use virtualenv here](https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/).

```
git clone https://github.com/juannat95/video-crawler.git
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Usage

`python scrape_youtube_meta.py --input ./sample/youtube_list.csv --output ./sample`

Feel free to remove any sections that aren't applicable to your project.

## To-Do
- [x] Retrieve basic metadata: Title
- [x] Retrieve more advanced metadata (part I): Views, Likes, Dislikes
- [ ] Retrieve more advanced metatada (part II): Hashtags, Description
- [ ] Scrape video links based on user's own keywords
- [ ] Download and manipulate videos if given links 

## Support

Please [open an issue](https://github.com/juannat95/video-crawler/issues/new) for support.
