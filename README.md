Web Crawler
===========
A simple web crawler created using beautiful soup, this was created as a workshop demo for [**Path to Python**](https://www.facebook.com/events/835260999876079/)

Installation
------------
* Setup virtual environment, as shown [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenv)
* Setup virtual environment wrapper, as shown [here](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#python-versions)
* Create a virtual environment for our project `mkvirtualenv web-crawler`
* Once inside the virtual env install all project dependencies by running `pip install -r requirements.txt`

Running the crawler
-------------------
* Run the crawler using `python crawler.py [seed_url] [max_depth]`
* In order to run the sample_site, go into the folder type `python -m SimpleHTTPServer`