# Arxiv Sanity Downloader

## Purpose:

This is a short python script that logs into your [arxiv-sanity](http://arxiv-sanity.com/) account, 
and downloads all the papers saved in your library under the actual titles, to 
save you hassle on having to manually download and rename the files.

## Requirements:

* Selenium with Chromedriver (any driver will do but you might have to
modify code a bit). You will have to paste the path to your chromedriver into
code.

* requests

* pathlib

## Usage:

1. Enter your username and password for arxiv sanity into the script

2. Copy the path to your Chromedriver into the script

3. Enter names of the folders you want to be scanned for papers (relative to the folder
the script is in. By default "Read", and "Unread")

4. Enter the name of the folder you want papers to be downloaded into

5. Run the script 
